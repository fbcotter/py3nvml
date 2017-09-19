from __future__ import absolute_import
from __future__ import print_function

import logging
import os
import warnings
from py3nvml import py3nvml


def grab_gpus(num_gpus=1, gpu_select=None, gpu_fraction=1.0):
    """
    Checks for gpu availability and sets CUDA_VISIBLE_DEVICES as such.

    Note that this function does not do anything to 'reserve' gpus, it only
    limits what GPUS your program can see by altering the CUDA_VISIBLE_DEVICES
    variable. Other programs can still come along and snatch your gpu. This
    function is more about preventing **you** from stealing someone else's GPU.

    If more than 1 GPU is requested but the full amount are available, then it
    will set the CUDA_VISIBLE_DEVICES variable to see all the available GPUs.
    A warning is generated in this case.

    If one or more GPUs were requested and none were available, a ValueError
    will be raised. Before raising it, the CUDA_VISIBLE_DEVICES will be set to a
    blank string. This means the calling function can catch this error and
    proceed if it chooses to only use the CPU, and it should still be protected
    against putting processes on a busy GPU.

    You can call this function with num_gpus=0 to blank out the
    CUDA_VISIBLE_DEVICES environment variable.

    Parameters
    ----------
    num_gpus : int
        How many gpus your job needs (optional)
    gpu_select : iterable
        A single int or an iterable of ints indicating gpu numbers to
        search through.  If left blank, will search through all gpus.
    gpu_fraction : float
        The fractional of a gpu memory that must be free for the script to see
        the gpu as free. Defaults to 1. Useful if someone has grabbed a tiny
        amount of memory on a gpu but isn't using it.

    Returns
    -------
    success : int
        Number of gpus 'grabbed'

    Raises
    ------
    RuntimeWarning
        If couldn't connect with NVIDIA drivers.
    ValueError
        If the gpu_select option was not understood (can fix by leaving this
        field blank, providing an int or an iterable of ints).
    ValueError
        If 1 or more gpus were requested and none were available.
    """
    # Set the visible devices to blank.
    os.environ['CUDA_VISIBLE_DEVICES'] = ""

    if num_gpus == 0:
        return 0

    # Try connect with NVIDIA drivers
    logger = logging.getLogger(__name__)
    try:
        py3nvml.nvmlInit()
    except:
        str_ = """Couldn't connect to nvml drivers. Check they are installed correctly.
                  Proceeding on cpu only..."""
        warnings.warn(str_, RuntimeWarning)
        logger.warn(str_)
        return

    numDevices = py3nvml.nvmlDeviceGetCount()
    gpu_free = [False]*numDevices

    # Flag which gpus we can check
    if gpu_select is None:
        gpu_check = [True] * 8
    else:
        gpu_check = [False] * 8
        try:
            gpu_check[gpu_select] = True
        except TypeError:
            try:
                for i in gpu_select:
                    gpu_check[i] = True
            except:
                raise ValueError('''Please provide an int or an iterable of ints
                    for gpu_select''')

    # Print out GPU device info. Useful for debugging.
    for i in range(numDevices):
        # If the gpu was specified, examine it
        if not gpu_check[i]:
            continue

        handle = py3nvml.nvmlDeviceGetHandleByIndex(i)
        info = py3nvml.nvmlDeviceGetMemoryInfo(handle)

        str_ = "GPU {}:\t".format(i) + \
               "Used Mem: {:>6}MB\t".format(info.used/(1024*1024)) + \
               "Total Mem: {:>6}MB".format(info.total/(1024*1024))
        logger.debug(str_)

    # Now check if any devices are suitable
    for i in range(numDevices):
        # If the gpu was specified, examine it
        if not gpu_check[i]:
            continue

        handle = py3nvml.nvmlDeviceGetHandleByIndex(i)
        info = py3nvml.nvmlDeviceGetMemoryInfo(handle)

        # Sometimes GPU has a few MB used when it is actually free
        if (info.free+10)/info.total >= gpu_fraction:
            gpu_free[i] = True
        else:
            logger.info('GPU {} has processes on it. Skipping.'.format(i))

    py3nvml.nvmlShutdown()

    # Now check whether we can create the session
    if sum(gpu_free) == 0:
        raise ValueError("Could not find enough GPUs for your job")
    else:
        if sum(gpu_free) >= num_gpus:
            # only use the first num_gpus gpus. Hide the rest from greedy
            # tensorflow
            available_gpus = [i for i, x in enumerate(gpu_free) if x]
            use_gpus = ','.join(list(str(s) for s in available_gpus[:num_gpus]))
            logger.debug('{} Gpus found free'.format(sum(gpu_free)))
            logger.info('Using {}'.format(use_gpus))
            os.environ['CUDA_VISIBLE_DEVICES'] = use_gpus
            return num_gpus
        else:
            # use everything we can.
            s = "Only {} GPUs found but {}".format(sum(gpu_free), num_gpus) + \
                "requested. Allocating these and continuing."
            warnings.warn(s, RuntimeWarning)
            logger.warn(s)
            available_gpus = [i for i, x in enumerate(gpu_free) if x]
            use_gpus = ','.join(list(str(s) for s in available_gpus))
            logger.debug('{} Gpus found free'.format(sum(gpu_free)))
            logger.info('Using {}'.format(use_gpus))
            os.environ['CUDA_VISIBLE_DEVICES'] = use_gpus
            return sum(gpu_free)

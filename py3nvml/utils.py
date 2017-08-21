from __future__ import absolute_import
from __future__ import print_function

import logging
import os
import warnings
from py3nvml import py3nvml


def grab_gpus(num_gpus=1,gpu_select=None, gpu_fraction=1.0):
    """
    Checks for gpu availability and sets CUDA_VISIBLE_DEVICES as such.

    Will first search for a GPU that is available and will set the correct
    environment variables so we don't try to use it. Calling this function will
    set the environment variable CUDA_VISIBLE_DEVICES, regardless of whether it
    succeeds or not.

    This will be useful if it fails to find any free GPUs and
    raises an exception, the caller could then try themselves anyway and
    tensorflow will grab whatever it pleases, and potentially disrupt the other
    jobs. Now, if create_session fails, it will still have set the
    CUDA_VISIBLE_DEVICES env to be "".

    :param num_gpus (optional) how many gpus your job needs
    :param gpu_select (optional) a single int or an iterable of ints gpus to
        search through.  If left blank, will search through all gpus.
    :param gpu_fraction (optional) the fractional of a gpu memory that must be
        free for the script to see the gpu as free. Defaults to 1. Useful if
        someone has grabbed a tiny amount of memory on a gpu but isn't using
        it.

    :raises RuntimeWarning: If couldn't connect with NVIDIA drivers
    :raises ValueError: If the function fails (either if the parameters were not
        understood, or the GPUs were full.
    """

    # Set the visible devices to blank.
    os.environ['CUDA_VISIBLE_DEVICES'] = ""

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
            return
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
            return

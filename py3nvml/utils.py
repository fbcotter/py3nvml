from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import logging
import os
import warnings
from py3nvml import py3nvml


def grab_gpus(num_gpus=1, gpu_select=None, gpu_fraction=0.95, max_procs=-1,
              env_set_ok=True):
    """
    Checks for gpu availability and sets CUDA_VISIBLE_DEVICES as such.

    Note that this function does not do anything to 'reserve' gpus, it only
    limits what GPUS your program can see by altering the CUDA_VISIBLE_DEVICES
    variable. Other programs can still come along and snatch your gpu. This
    function is more about preventing **you** from stealing someone else's GPU.

    If more than 1 GPU is requested but not all were available, then it
    will set the CUDA_VISIBLE_DEVICES variable to see all the available GPUs.
    A warning is generated in this case.

    If one or more GPUs were requested and none were available, a Warning
    will be raised. Before raising it, the CUDA_VISIBLE_DEVICES will be set to
    a blank string. This means the calling function can ignore this warning and
    proceed if it chooses to only use the CPU, and it should still be protected
    against putting processes on a busy GPU.

    You can call this function with num_gpus=0 to blank out the
    CUDA_VISIBLE_DEVICES environment variable.

    Parameters
    ----------
    num_gpus : int
        How many gpus your job needs (optional). Can set to -1 to take all
        remaining available GPUs.
    gpu_select : iterable
        A single int or an iterable of ints indicating gpu numbers to
        search through. If None, will search through all gpus.
    gpu_fraction : float
        The fractional of a gpu memory that must be free for the script to see
        the gpu as free. Defaults to 1. Useful if someone has grabbed a tiny
        amount of memory on a gpu but isn't using it.
    max_procs : int
        Maximum number of processes allowed on a GPU (as well as memory
        restriction).
    env_set_ok : bool
        If true, will complain if CUDA_VISIBLE_DEVICES is already set.

    Returns
    -------
    success : int
        Number of gpus 'grabbed'

    Raises
    ------
    RuntimeWarning
        If couldn't connect with NVIDIA drivers.
        If 1 or more gpus were requested and none were available.
        Will NOT raise a RuntimeWarning for mismatch in GPU availability if
        `num_gpus` is -1.
    ValueError
        If the gpu_select option was not understood (can fix by leaving this
        field blank, providing an int or an iterable of ints).
    """
    if not env_set_ok and 'CUDA_VISIBLE_DEVICES' in os.environ.keys():
        raise ValueError('Trying to set CUDA_VISIBLE_DEVICES but it has been '
                         'set already. Specify env_set_ok=True to avoid this '
                         'error.')

    # Set the visible devices to blank.
    os.environ['CUDA_VISIBLE_DEVICES'] = ""

    if num_gpus == 0:
        return 0

    # Try connect with NVIDIA drivers
    logger = logging.getLogger(__name__)
    try:
        py3nvml.nvmlInit()
    except:
        str_ = "Couldn't connect to nvml drivers. Check they are installed " \
            "correctly.\nProceeding on cpu only..."
        warnings.warn(str_, RuntimeWarning)
        logger.warn(str_)
        return 0

    numDevices = py3nvml.nvmlDeviceGetCount()
    gpu_free = [False]*numDevices

    warn_about_fewer_gpus = True
    if num_gpus == -1:
        num_gpus = numDevices
        warn_about_fewer_gpus = False

    # Flag which gpus we can check
    if gpu_select is None:
        gpu_check = [True] * numDevices
    else:
        gpu_check = [False] * numDevices
        try:
            gpu_check[gpu_select] = True
        except TypeError:
            try:
                for i in gpu_select:
                    gpu_check[i] = True
            except:
                raise ValueError('Please set gpu_select to None, an int or an'
                                 'iterable of ints.')

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

    # Check the number of procs running on each gpu
    if max_procs >= 0:
        procs_ok = get_free_gpus(max_procs=max_procs)
    else:
        procs_ok = [True, ] * numDevices

    # Now check if any devices are suitable
    for i in range(numDevices):
        # If the gpu was not specified, skip it
        if gpu_check[i] and procs_ok[i]:

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
        warnings.warn("Could not find enough GPUs for your job", RuntimeWarning)
        logger.warn(str_)
        return 0
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
        elif warn_about_fewer_gpus:
            # use everything we can.
            s = "Only {} GPUs found but {} ".format(sum(gpu_free), num_gpus) + \
                "requested. Allocating these and continuing."
            warnings.warn(s, RuntimeWarning)
            logger.warn(s)
            available_gpus = [i for i, x in enumerate(gpu_free) if x]
            use_gpus = ','.join(list(str(s) for s in available_gpus))
            logger.debug('{} Gpus found free'.format(sum(gpu_free)))
            logger.info('Using {}'.format(use_gpus))
            os.environ['CUDA_VISIBLE_DEVICES'] = use_gpus
            return sum(gpu_free)


def try_get_info(f, h, default='N/A'):
    try:
        v = f(h)
    except py3nvml.NVMLError_NotSupported:
        v = default
    return v


def get_free_gpus(max_procs=0):
    """
    Checks the number of processes running on your GPUs.

    Parameters
    ----------
    max_procs : int
        Maximum number of procs allowed to run on a gpu for it to be considered
        'available'

    Returns
    -------
    availabilities : list(bool)
        List of length N for an N-gpu system. The nth value will be true, if the
        nth gpu had at most max_procs processes running on it. Set to 0 to look
        for gpus with no procs on it.

    Note
    ----
    If function can't query the driver will return an empty list rather than raise an
    Exception.
    """
    # Try connect with NVIDIA drivers
    logger = logging.getLogger(__name__)
    try:
        py3nvml.nvmlInit()
    except:
        str_ = """Couldn't connect to nvml drivers. Check they are installed correctly."""
        warnings.warn(str_, RuntimeWarning)
        logger.warn(str_)
        return []

    num_gpus = py3nvml.nvmlDeviceGetCount()
    gpu_free = [False]*num_gpus
    for i in range(num_gpus):
        try:
            h = py3nvml.nvmlDeviceGetHandleByIndex(i)
        except:
            continue

        procs = try_get_info(py3nvml.nvmlDeviceGetComputeRunningProcesses, h,
                             ['something'])
        if len(procs) <= max_procs:
            gpu_free[i] = True

    py3nvml.nvmlShutdown()
    return gpu_free


def get_num_procs():
    """ Gets the number of processes running on each gpu

    Returns
    -------
    num_procs : list(int)
        Number of processes running on each gpu

    Note
    ----
    If function can't query the driver will return an empty list rather than raise an
    Exception.

    Note
    ----
    If function can't get the info from the gpu will return -1 in that gpu's place
    """
    # Try connect with NVIDIA drivers
    logger = logging.getLogger(__name__)
    try:
        py3nvml.nvmlInit()
    except:
        str_ = """Couldn't connect to nvml drivers. Check they are installed correctly."""
        warnings.warn(str_, RuntimeWarning)
        logger.warn(str_)
        return []

    num_gpus = py3nvml.nvmlDeviceGetCount()
    gpu_procs = [-1]*num_gpus
    for i in range(num_gpus):
        try:
            h = py3nvml.nvmlDeviceGetHandleByIndex(i)
        except:
            continue
        procs = try_get_info(py3nvml.nvmlDeviceGetComputeRunningProcesses, h,
                             ['something'])
        gpu_procs[i] = len(procs)

    py3nvml.nvmlShutdown()
    return gpu_procs

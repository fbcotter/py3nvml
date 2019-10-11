from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
from time import sleep
from py3nvml.py3nvml import *
import pytest
from py3nvml.utils import grab_gpus, get_free_gpus
import os

def pop_if_set():
    if "CUDA_VISIBLE_DEVICES" in os.environ.keys():
        os.environ.pop("CUDA_VISIBLE_DEVICES")

def test_readme1():
    nvmlInit()
    print("Driver Version: {}".format(nvmlSystemGetDriverVersion()))
    deviceCount = nvmlDeviceGetCount()
    for i in range(deviceCount):
        handle = nvmlDeviceGetHandleByIndex(i)
        print("Device {}: {}".format(i, nvmlDeviceGetName(handle)))

    nvmlShutdown()


def test_grabgpus():
    pop_if_set()
    res = grab_gpus(0)
    assert os.environ['CUDA_VISIBLE_DEVICES'] == ''
    assert res == 0

def test_grabgpus2():
    pop_if_set()
    res = grab_gpus(1)
    assert len(os.environ['CUDA_VISIBLE_DEVICES']) > 0
    assert res == 1

def test_grabgpus3():
    pop_if_set()
    res = grab_gpus(100)
    assert len(os.environ['CUDA_VISIBLE_DEVICES']) < len(','.join([str(x) for x in range(100)]))
    nvmlInit()
    assert res <= nvmlDeviceGetCount()
    nvmlShutdown()


def test_grabgpus4():
    pop_if_set()
    grab_gpus(5, gpu_select=range(3,8))
    assert '0' not in os.environ['CUDA_VISIBLE_DEVICES']
    assert '1' not in os.environ['CUDA_VISIBLE_DEVICES']
    assert '2' not in os.environ['CUDA_VISIBLE_DEVICES']

def test_get_free_gpus():
    pass

def test_called_twice():
    pop_if_set()
    grab_gpus(1)
    grab_gpus(1, env_set_ok=True)
    with pytest.raises(ValueError):
        grab_gpus(1, env_set_ok=False)

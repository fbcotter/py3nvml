# py3nvml

Python 3 compatible bindings to the NVIDIA Management Library. Can be used to
query the state of the GPUs on your system. This was ported from the NVIDIA
provided python bindings 
[nvidia-ml-py](https://pypi.python.org/pypi/nvidia-ml-py/7.352.0), which only 
supported python 2. I have forked from version 7.352.0. The old library was 
itself a wrapper around the [NVIDIA
Management Library](http://developer.nvidia.com/nvidia-management-library-nvml).
 
In addition to the functions to query the state of the GPU, I have written
a function to 'restrict' the available GPUs by setting the CUDA_VISIBLE_DEVICES
environment variable. See the Utils section below for more info.

# Requires
Python 3.5+.

# Installation 
## From PyPi

    $ pip install py3nvml

## From GitHub
Direct install from github (useful if you use pip freeze)
    
    $ pip install -e git+https://github.com/fbcotter/py3nvml#egg=py3nvml

Download and pip install from Git:

    $ git clone https://github.com/fbcotter/py3nvml
    $ cd py3nvml
    $ pip install .

# Package Description
## Utils (added by me - not ported from NVIDIA library)

You can call the grab_gpus(num_gpus, gpu_select) function to check the
available gpus and set the CUDA_VISIBLE_DEVICES environment variable as need
be. This is useful if you have a shared resource, and are using a library like
tensorflow where calls to tf.Session() grabs all available gpus.

E.g.

    >>> import py3nvml
    >>> py3nvml.grab_gpus(3)
    >>> sess = tf.Session() # now we only grab 3 gpus!

Or the following will grab 2 gpus from the first 4 (and leave any higher gpus untouched)
    
    >>> import py3nvml
    >>> py3nvml.grab_gpus(2, range(4))
    >>> sess = tf.Session() 

This will look for 3 available gpus in the range of gpus from 2 to 6. The range
option is not necessary, and it only serves to restrict the search space for
the grab_gpus.

## Special TF Utils usage (deprecated and will be removed in future)

If you are using Tensorflow, I have included a helper function to query the
gpus and create a session. As py3nvml should work without tensorflow, you have
to import this module separately. I.e.,

    >>> import py3nvml # optional
    >>> from py3nvml.tf_utils import create_session
    >>> sess = create_session(num_gpus=3,gpu_select=range(6),graph=mygraph)

Have a closer look at the docstring for create_session, but the above example
attempst to create a session using 3 gpus, by searching the first 6 gpus for
available memory. 

## Regular Usage (below here is everything ported from pynvml)

    >>> from py3nvml.py3nvml import *
    >>> nvmlInit()
    >>> print("Driver Version: {}".format(str(nvmlSystemGetDriverVersion())))
    Driver Version: 352.00
    >>> deviceCount = nvmlDeviceGetCount()
    >>> for i in range(deviceCount):
    ...     handle = nvmlDeviceGetHandleByIndex(i)
    ...     print("Device {}: {}".format(i, str(nvmlDeviceGetName(handle))))
    ... 
    Device 0 : Tesla K40c
    
    >>> nvmlShutdown()

Additionally, see py3nvml.nvidia_smi.py.  A sample application that prints out
the same as the command line:

    nvidia-smi -q -x

Can be done with:

    >>> import py3nvml.nvidia_smi as smi
    >>> print(smi.XmlDeviceQuery())

You will notice that a lot of the calls are wrapped with str() functions, as
the underlying NVIDIA library returns bytes objects most of the time. 

## Functions
Python methods wrap NVML functions, implemented in a C shared library.
Each function's use is the same with the following exceptions:

- Instead of returning error codes, failing error codes are raised as 
  Python exceptions.

    ```python
    try:
        nvmlDeviceGetCount()
    except NVMLError as error:
        print error
    ```
    Prints:
    ```
    Uninitialized
    ```

- C function output parameters are returned from the corresponding
  Python function left to right. Eg the C function:
    
    ```C
    nvmlReturn_t nvmlDeviceGetEccMode(nvmlDevice_t device,
                                      nvmlEnableState_t *current,
                                      nvmlEnableState_t *pending);
    ```
    Can be called like so:
    ```python
    >>> nvmlInit()
    >>> handle = nvmlDeviceGetHandleByIndex(0)
    >>> (current, pending) = nvmlDeviceGetEccMode(handle)
    ```

- C structs are converted into Python classes.

    E.g. the C struct:
    ```C
    nvmlReturn_t DECLDIR nvmlDeviceGetMemoryInfo(nvmlDevice_t device,
                                                 nvmlMemory_t *memory);
    typedef struct nvmlMemory_st {
        unsigned long long total;
        unsigned long long free;
        unsigned long long used;
    } nvmlMemory_t;
    ```

    Becomes:
    ```python
    >>> info = nvmlDeviceGetMemoryInfo(handle)
    >>> print "Total memory:", info.total
    Total memory: 5636292608
    >>> print "Free memory:", info.free
    Free memory: 5578420224
    >>> print "Used memory:", info.used
    Used memory: 57872384

- Python handles string buffer creation.
    E.g. the C function:
    ```C
    nvmlReturn_t nvmlSystemGetDriverVersion(char* version,
                                            unsigned int length);
    ```
    Can be called like so:
    ```python
    >>> version = nvmlSystemGetDriverVersion();
    >>> nvmlShutdown()
    ```

For usage information see the NVML documentation.

## Variables
All meaningful NVML constants and enums are exposed in Python.

The NVML_VALUE_NOT_AVAILABLE constant is not used.  Instead None is mapped to the field.

## Release Notes
Version 2.285.0
- Added new functions for NVML 2.285.  See NVML documentation for more information.
- Ported to support Python 3.0 and Python 2.0 syntax.
- Added nvidia_smi.py tool as a sample app.
Version 3.295.0
- Added new functions for NVML 3.295.  See NVML documentation for more information.
- Updated nvidia_smi.py tool
  - Includes additional error handling
Version 4.304.0
- Added new functions for NVML 4.304.  See NVML documentation for more information.
- Updated nvidia_smi.py tool
Version 4.304.3
- Fixing nvmlUnitGetDeviceCount bug
Version 5.319.0
- Added new functions for NVML 5.319.  See NVML documentation for more information.
Version 6.340.0
- Added new functions for NVML 6.340.  See NVML documentation for more information.
Version 7.346.0
- Added new functions for NVML 7.346.  See NVML documentation for more information.
Version 7.352.0
- Added new functions for NVML 7.352.  See NVML documentation for more information.

## COPYRIGHT
Copyright (c) 2011-2015, NVIDIA Corporation.  All rights reserved.

## LICENSE
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

- Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.

- Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

- Neither the name of the NVIDIA Corporation nor the names of its contributors
may be used to endorse or promote products derived from this software without
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.



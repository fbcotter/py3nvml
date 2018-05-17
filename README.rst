py3nvml
=======

Python 3 compatible bindings to the NVIDIA Management Library. Can be used to
query the state of the GPUs on your system. This was ported from the NVIDIA
provided python bindings `nvidia-ml-py`__, which only 
supported python 2. I have forked from version 7.352.0. The old library was 
itself a wrapper around the `NVIDIA Management Library`__.

__ https://pypi.python.org/pypi/nvidia-ml-py/7.352.0
__ http://developer.nvidia.com/nvidia-management-library-nvml

In addition to these NVIDIA functions to query the state of the GPU, I have written
a couple functions/tools to help in using gpus (particularly for a shared
gpu server). These are:

- A function to 'restrict' the available GPUs by setting the `CUDA_VISIBLE_DEVICES` 
  environment variable. 
- A script for displaying a differently formatted nvidia-smi.

See the Utils section below for more info.

Requires
--------
Python 3.5+.

Installation 
------------
From PyPi::

    $ pip install py3nvml

From GitHub::
    
    $ pip install -e git+https://github.com/fbcotter/py3nvml#egg=py3nvml

Or, download and pip install:: 

    $ git clone https://github.com/fbcotter/py3nvml
    $ cd py3nvml
    $ pip install .

.. _utils-label:

Package Description
-------------------

Utils 
'''''
(Added by me - not ported from NVIDIA library)

grab_gpus
~~~~~~~~~

You can call the :code:`grab_gpus(num_gpus, gpu_select)` function to check the
available gpus and set the `CUDA_VISIBLE_DEVICES` environment variable as need
be. It determines if a GPU is available by checking if the memory-usage is 0%. 

I have found this useful as I have a shared gpu server and like to use
tensorflow which is very greedy and calls to :code:`tf.Session()` grabs all available gpus.

E.g.

.. code:: python

    import py3nvml
    py3nvml.grab_gpus(3)
    sess = tf.Session() # now we only grab 3 gpus!

Or the following will grab 2 gpus from the first 4 (and leave any higher gpus untouched)

.. code:: python
    
    import py3nvml
    py3nvml.grab_gpus(num_gpus=2, gpu_select=[0,1,2,3])
    sess = tf.Session() 

This will look for 3 available gpus in the range of gpus from 0 to 3. The range
option is not necessary, and it only serves to restrict the search space for
the grab_gpus. 

You can adjust the memory threshold for determining if a GPU is free/used with
the :code:`gpu_fraction` parameter (default is 1):

.. code:: python
    
    import py3nvml
    # Will allocate a GPU if less than 10% of its memory is being used
    py3nvml.grab_gpus(num_gpus=2, gpu_fraction=0.9)
    sess = tf.Session() 

This function has no return codes but may raise some warnings/exceptions:

- If the method could not connect to any NVIDIA gpus, it will raise
  a RuntimeWarning. 
- If it could connect to the GPUs, but there were none available, it will 
  raise a ValueError. 
- If it could connect to the GPUs but not enough were available (i.e. more than
  1 was requested), it will take everything it can and raise a RuntimeWarning.

py3smi
~~~~~~
I found the default `nvidia-smi` output was missing some useful info, so made use of the
`py3nvml/nvidia_smi.py` module to query the device and return XML info on the
GPUs, and then defined my own printout. I have included this as a script in
`scripts/py3smi`. Running pip install will now put this script in your python's
bin, and you'll be able to run it from the command line. Here is a comparison of
the two outputs:

.. image:: https://i.imgur.com/TvdfkFE.png

.. image:: https://i.imgur.com/UPSHr8k.png

For py3smi, you can specify an update period so it will refresh the feed every
few seconds. I.e., similar to :code:`watch -n5 nvidia-smi`, you can run
:code:`py3smi -l 5`.

Regular Usage 
'''''''''''''
(below here is everything ported from pynvml)

.. code:: python

    from py3nvml.py3nvml import *
    nvmlInit()
    print("Driver Version: {}".format(nvmlSystemGetDriverVersion()))
    # e.g. will print:
    #   Driver Version: 352.00
    deviceCount = nvmlDeviceGetCount()
    for i in range(deviceCount):
        handle = nvmlDeviceGetHandleByIndex(i)
        print("Device {}: {}".format(i, nvmlDeviceGetName(handle)))
    # e.g. will print:
    #  Device 0 : Tesla K40c
    #  Device 1 : Tesla K40c
    
    nvmlShutdown()

Additionally, see `py3nvml.nvidia_smi.py`. This does the equivalent of the
`nvidia-smi` command:: 

    nvidia-smi -q -x

With

.. code:: python

    import py3nvml.nvidia_smi as smi
    print(smi.XmlDeviceQuery())


Function description
''''''''''''''''''''
As stated above, the pynvml library consists of python methods which wrap 
several NVML functions, implemented in a C shared library.
Each function's use is the same with the following exceptions:

- Instead of returning error codes, failing error codes are raised as 
  Python exceptions. E.g. They could be wrapped with exception handlers.

  .. code:: python

    try:
        nvmlDeviceGetCount()
    except NVMLError as error:
        print(error)


- C function output parameters are returned from the corresponding
  Python function left to right. Eg the C function:
    
  .. code:: c

    nvmlReturn_t nvmlDeviceGetEccMode(nvmlDevice_t device,
                                      nvmlEnableState_t *current,
                                      nvmlEnableState_t *pending);

  Can be called like so:

  .. code:: python

    nvmlInit()
    handle = nvmlDeviceGetHandleByIndex(0)
    (current, pending) = nvmlDeviceGetEccMode(handle)

- C structs are converted into Python classes. E.g. the C struct:

  .. code:: c

    nvmlReturn_t DECLDIR nvmlDeviceGetMemoryInfo(nvmlDevice_t device,
                                                 nvmlMemory_t *memory);
    typedef struct nvmlMemory_st {
        unsigned long long total;
        unsigned long long free;
        unsigned long long used;
    } nvmlMemory_t;

  Becomes:

  .. code:: python

    info = nvmlDeviceGetMemoryInfo(handle)
    print("Total memory: {}".format(info.total))
    # will print:
    #   Total memory: 5636292608
    print("Free memory: {}".format(info.free))
    # will print:
    #   Free memory: 5578420224
    print("Used memory: ".format(info.used))
    # will print:
    #   Used memory: 57872384

- Python handles string buffer creation.  E.g. the C function:

  .. code:: c

    nvmlReturn_t nvmlSystemGetDriverVersion(char* version,
                                            unsigned int length);

  Can be called like so:

  .. code:: python

    version = nvmlSystemGetDriverVersion()
    nvmlShutdown()

For usage information see the NVML documentation.

Variables
~~~~~~~~~
All meaningful NVML constants and enums are exposed in Python.

The `NVML_VALUE_NOT_AVAILABLE` constant is not used.  Instead None is mapped to the field.

Release Notes (for pynvml)
--------------------------
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

COPYRIGHT
---------
Copyright (c) 2011-2015, NVIDIA Corporation.  All rights reserved.

LICENSE
-------
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



#####
# Copyright (c) 2011-2015, NVIDIA Corporation.  All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright notice,
#      this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the NVIDIA Corporation nor the names of its
#      contributors may be used to endorse or promote products derived from
#      this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGE.
#####

##
# Python bindings for the NVML library
##
from ctypes import *    # noqa
from ctypes import c_uint
import sys
import os
import threading
import string
from enum import Enum

# C Type mappings #
# Enums
_nvmlEnableState_t = c_uint
NVML_FEATURE_DISABLED = 0
NVML_FEATURE_ENABLED = 1
class nvmlEnableState_t(Enum):
    NVML_FEATURE_DISABLED = 0
    NVML_FEATURE_ENABLED = 1


_nvmlBrandType_t = c_uint
NVML_BRAND_UNKNOWN = 0
NVML_BRAND_QUADRO = 1
NVML_BRAND_TESLA = 2
NVML_BRAND_NVS = 3
NVML_BRAND_GRID = 4
NVML_BRAND_GEFORCE = 5
NVML_BRAND_TITAN = 6
NVML_BRAND_COUNT = 7
class nvmlBrandType_t(Enum):
    NVML_BRAND_UNKNOWN = 0
    NVML_BRAND_QUADRO = 1
    NVML_BRAND_TESLA = 2
    NVML_BRAND_NVS = 3
    NVML_BRAND_GRID = 4
    NVML_BRAND_GEFORCE = 5
    NVML_BRAND_TITAN = 6
    NVML_BRAND_COUNT = 7


_nvmlTemperatureThresholds_t = c_uint
NVML_TEMPERATURE_THRESHOLD_SHUTDOWN = 0
NVML_TEMPERATURE_THRESHOLD_SLOWDOWN = 1
NVML_TEMPERATURE_THRESHOLD_MEM_MAX = 2
NVML_TEMPERATURE_THRESHOLD_GPU_MAX = 3
NVML_TEMPERATURE_THRESHOLD_COUNT = 4
class nvmlTemperatureThresholds_t(Enum):
    """
    // Temperature at which the GPU will shut down for HW protection
    NVML_TEMPERATURE_THRESHOLD_SHUTDOWN = 0,
    // Temperature at which the GPU will begin HW slowdown
    NVML_TEMPERATURE_THRESHOLD_SLOWDOWN = 1,
    // Memory Temperature at which the GPU will begin SW slowdown
    NVML_TEMPERATURE_THRESHOLD_MEM_MAX  = 2,
    // GPU Temperature at which the GPU can be throttled below base clock
    NVML_TEMPERATURE_THRESHOLD_GPU_MAX  = 3,
    """
    NVML_TEMPERATURE_THRESHOLD_SHUTDOWN = 0
    NVML_TEMPERATURE_THRESHOLD_SLOWDOWN = 1
    NVML_TEMPERATURE_THRESHOLD_MEM_MAX = 2
    NVML_TEMPERATURE_THRESHOLD_GPU_MAX = 3
    NVML_TEMPERATURE_THRESHOLD_COUNT = 4


_nvmlTemperatureSensors_t = c_uint
NVML_TEMPERATURE_GPU = 0
NVML_TEMPERATURE_COUNT = 1
class nvmlTemperatureSensors_t(Enum):
    """
    NVML_TEMPERATURE_GPU      = 0,    //!< Temperature sensor for the GPU die
    """
    NVML_TEMPERATURE_GPU = 0
    NVML_TEMPERATURE_COUNT = 1

_nvmlComputeMode_t = c_uint
# !< Default compute mode -- multiple contexts per device
# !< Support Removed
# !< Compute-prohibited mode -- no contexts per device
# !< Compute-exclusive-process mode -- only one context per device, usable from multiple threads at a time
NVML_COMPUTEMODE_DEFAULT = 0
NVML_COMPUTEMODE_EXCLUSIVE_THREAD = 1
NVML_COMPUTEMODE_PROHIBITED = 2
NVML_COMPUTEMODE_EXCLUSIVE_PROCESS = 3
NVML_COMPUTEMODE_COUNT = 4
class nvmlComputeMode_t(Enum):
    NVML_COMPUTEMODE_DEFAULT = 0
    NVML_COMPUTEMODE_EXCLUSIVE_THREAD = 1
    NVML_COMPUTEMODE_PROHIBITED = 2
    NVML_COMPUTEMODE_EXCLUSIVE_PROCESS = 3
    NVML_COMPUTEMODE_COUNT = 4

_nvmlMemoryLocation_t = c_uint
NVML_MEMORY_LOCATION_L1_CACHE = 0
NVML_MEMORY_LOCATION_L2_CACHE = 1
NVML_MEMORY_LOCATION_DRAM = 2
NVML_MEMORY_LOCATION_DEVICE_MEMORY = 2
NVML_MEMORY_LOCATION_REGISTER_FILE = 3
NVML_MEMORY_LOCATION_TEXTURE_MEMORY = 4
NVML_MEMORY_LOCATION_TEXTURE_SHM = 5
NVML_MEMORY_LOCATION_CBU = 6
NVML_MEMORY_LOCATION_SRAM = 7
NVML_MEMORY_LOCATION_COUNT = 8
class nvmlMemoryLocation_t(Enum):
    NVML_MEMORY_LOCATION_L1_CACHE = 0
    NVML_MEMORY_LOCATION_L2_CACHE = 1
    NVML_MEMORY_LOCATION_DRAM = 2
    NVML_MEMORY_LOCATION_DEVICE_MEMORY = 2
    NVML_MEMORY_LOCATION_REGISTER_FILE = 3
    NVML_MEMORY_LOCATION_TEXTURE_MEMORY = 4
    NVML_MEMORY_LOCATION_TEXTURE_SHM = 5
    NVML_MEMORY_LOCATION_CBU = 6
    NVML_MEMORY_LOCATION_SRAM = 7
    NVML_MEMORY_LOCATION_COUNT = 8


# These are deprecated, instead use _nvmlMemoryErrorType_t
_nvmlEccBitType_t = c_uint
NVML_SINGLE_BIT_ECC = 0
NVML_DOUBLE_BIT_ECC = 1
NVML_ECC_ERROR_TYPE_COUNT = 2

_nvmlEccCounterType_t = c_uint
NVML_VOLATILE_ECC = 0
NVML_AGGREGATE_ECC = 1
NVML_ECC_COUNTER_TYPE_COUNT = 2
class nvmlEccCounterType_t(Enum):
    """
    // Volatile counts are reset each time the driver loads.
    NVML_VOLATILE_ECC      = 0,
    // Aggregate counts persist across reboots (i.e. for the lifetime of the
    // device)
    NVML_AGGREGATE_ECC     = 1,
    """
    NVML_VOLATILE_ECC = 0
    NVML_AGGREGATE_ECC = 1
    NVML_ECC_COUNTER_TYPE_COUNT = 2


_nvmlMemoryErrorType_t = c_uint
NVML_MEMORY_ERROR_TYPE_CORRECTED = 0
NVML_MEMORY_ERROR_TYPE_UNCORRECTED = 1
NVML_MEMORY_ERROR_TYPE_COUNT = 2
class nvmlMemoryErrorType_t(Enum):
    """
    /**
     * A memory error that was corrected
     *
     * For ECC errors, these are single bit errors
     * For Texture memory, these are errors fixed by resend
     */
    NVML_MEMORY_ERROR_TYPE_CORRECTED = 0,
    /**
     * A memory error that was not corrected
     *
     * For ECC errors, these are double bit errors
     * For Texture memory, these are errors where the resend fails
     */
    NVML_MEMORY_ERROR_TYPE_UNCORRECTED = 1,
    """
    NVML_MEMORY_ERROR_TYPE_CORRECTED = 0
    NVML_MEMORY_ERROR_TYPE_UNCORRECTED = 1
    NVML_MEMORY_ERROR_TYPE_COUNT = 2


_nvmlClockType_t = c_uint
NVML_CLOCK_GRAPHICS = 0
NVML_CLOCK_SM = 1
NVML_CLOCK_MEM = 2
NVML_CLOCK_VIDEO = 3
NVML_CLOCK_COUNT = 4
class nvmlClockType_t(Enum):
    NVML_CLOCK_GRAPHICS = 0
    NVML_CLOCK_SM = 1
    NVML_CLOCK_MEM = 2
    NVML_CLOCK_VIDEO = 3
    NVML_CLOCK_COUNT = 4


_nvmlDriverModel_t = c_uint
NVML_DRIVER_WDDM = 0
NVML_DRIVER_WDM = 1
class nvmlDriverModel_t(Enum):
    """
    // WDDM driver model -- GPU treated as a display device
    NVML_DRIVER_WDDM      = 0,
    // WDM (TCC) model (recommended) -- GPU treated as a generic device
    NVML_DRIVER_WDM       = 1
    """
    NVML_DRIVER_WDDM = 0
    NVML_DRIVER_WDM = 1


_nvmlPstates_t = c_uint
NVML_PSTATE_0 = 0
NVML_PSTATE_1 = 1
NVML_PSTATE_2 = 2
NVML_PSTATE_3 = 3
NVML_PSTATE_4 = 4
NVML_PSTATE_5 = 5
NVML_PSTATE_6 = 6
NVML_PSTATE_7 = 7
NVML_PSTATE_8 = 8
NVML_PSTATE_9 = 9
NVML_PSTATE_10 = 10
NVML_PSTATE_11 = 11
NVML_PSTATE_12 = 12
NVML_PSTATE_13 = 13
NVML_PSTATE_14 = 14
NVML_PSTATE_15 = 15
NVML_PSTATE_UNKNOWN = 32
class nvmlPstates_t(Enum):
    """
    Performance State 0 is maximum performance and 15 is minimum performance
    """
    NVML_PSTATE_0 = 0
    NVML_PSTATE_1 = 1
    NVML_PSTATE_2 = 2
    NVML_PSTATE_3 = 3
    NVML_PSTATE_4 = 4
    NVML_PSTATE_5 = 5
    NVML_PSTATE_6 = 6
    NVML_PSTATE_7 = 7
    NVML_PSTATE_8 = 8
    NVML_PSTATE_9 = 9
    NVML_PSTATE_10 = 10
    NVML_PSTATE_11 = 11
    NVML_PSTATE_12 = 12
    NVML_PSTATE_13 = 13
    NVML_PSTATE_14 = 14
    NVML_PSTATE_15 = 15
    NVML_PSTATE_UNKNOWN = 32


_nvmlInforomObject_t = c_uint
NVML_INFOROM_OEM = 0
NVML_INFOROM_ECC = 1
NVML_INFOROM_POWER = 2
NVML_INFOROM_COUNT = 3
class nvmlInforomObject_t(Enum):
    """
    // An object defined by OEM
    NVML_INFOROM_OEM            = 0,
    // The ECC object determining the level of ECC support
    NVML_INFOROM_ECC            = 1,
    // The power management object
    NVML_INFOROM_POWER          = 2,
    """
    NVML_INFOROM_OEM = 0
    NVML_INFOROM_ECC = 1
    NVML_INFOROM_POWER = 2
    NVML_INFOROM_COUNT = 3

_nvmlReturn_t = c_uint
NVML_SUCCESS = 0
NVML_ERROR_UNINITIALIZED = 1
NVML_ERROR_INVALID_ARGUMENT = 2
NVML_ERROR_NOT_SUPPORTED = 3
NVML_ERROR_NO_PERMISSION = 4
NVML_ERROR_ALREADY_INITIALIZED = 5
NVML_ERROR_NOT_FOUND = 6
NVML_ERROR_INSUFFICIENT_SIZE = 7
NVML_ERROR_INSUFFICIENT_POWER = 8
NVML_ERROR_DRIVER_NOT_LOADED = 9
NVML_ERROR_TIMEOUT = 10
NVML_ERROR_IRQ_ISSUE = 11
NVML_ERROR_LIBRARY_NOT_FOUND = 12
NVML_ERROR_FUNCTION_NOT_FOUND = 13
NVML_ERROR_CORRUPTED_INFOROM = 14
NVML_ERROR_GPU_IS_LOST = 15
NVML_ERROR_RESET_REQUIRED = 16
NVML_ERROR_OPERATING_SYSTEM = 17
NVML_ERROR_LIB_RM_VERSION_MISMATCH = 18
NVML_ERROR_IN_USE = 19
NVML_ERROR_MEMORY = 20
NVML_ERROR_NO_DATA = 21
NVML_ERROR_VGPU_ECC_NOT_SUPPORTED = 22
NVML_ERROR_UNKNOWN = 999

class nvmlReturn_t(Enum):
    """
    // The operation was successful
    NVML_SUCCESS = 0,
    // NVML was not first initialized with nvmlInit()
    NVML_ERROR_UNINITIALIZED = 1,
    // A supplied argument is invalid
    NVML_ERROR_INVALID_ARGUMENT = 2,
    // The requested operation is not available on target device
    NVML_ERROR_NOT_SUPPORTED = 3,
    // The current user does not have permission for operation
    NVML_ERROR_NO_PERMISSION = 4,
    // Deprecated: Multiple initializations are now allowed through ref counting
    NVML_ERROR_ALREADY_INITIALIZED = 5,
    // A query to find an object was unsuccessful
    NVML_ERROR_NOT_FOUND = 6,
    // An input argument is not large enough
    NVML_ERROR_INSUFFICIENT_SIZE = 7,
    //A device's external power cables are not properly attached
    NVML_ERROR_INSUFFICIENT_POWER = 8,
    // NVIDIA driver is not loaded
    NVML_ERROR_DRIVER_NOT_LOADED = 9,
    // User provided timeout passed
    NVML_ERROR_TIMEOUT = 10,
    // NVIDIA Kernel detected an interrupt issue with a GPU
    NVML_ERROR_IRQ_ISSUE = 11,
    // NVML Shared Library couldn't be found or loaded
    NVML_ERROR_LIBRARY_NOT_FOUND = 12,
    // Local version of NVML doesn't implement this function
    NVML_ERROR_FUNCTION_NOT_FOUND = 13,
    // infoROM is corrupted
    NVML_ERROR_CORRUPTED_INFOROM = 14,
    // The GPU has fallen off the bus or has otherwise become inaccessible
    NVML_ERROR_GPU_IS_LOST = 15,
    // The GPU requires a reset before it can be used again
    NVML_ERROR_RESET_REQUIRED = 16,
    // The GPU control device has been blocked by the operating system/cgroups
    NVML_ERROR_OPERATING_SYSTEM = 17,
    // RM detects a driver/library version mismatch
    NVML_ERROR_LIB_RM_VERSION_MISMATCH = 18,
    // An operation cannot be performed because the GPU is currently in use
    NVML_ERROR_IN_USE = 19,
    // Insufficient memory
    NVML_ERROR_MEMORY = 20,
    // No data
    NVML_ERROR_NO_DATA = 21,
    // The requested vgpu operation is not available on target device, becasue
    // ECC is enabled
    NVML_ERROR_VGPU_ECC_NOT_SUPPORTED = 22,
    // An internal driver error occurred
    NVML_ERROR_UNKNOWN = 999
    """
    NVML_SUCCESS = 0
    NVML_ERROR_UNINITIALIZED = 1
    NVML_ERROR_INVALID_ARGUMENT = 2
    NVML_ERROR_NOT_SUPPORTED = 3
    NVML_ERROR_NO_PERMISSION = 4
    NVML_ERROR_ALREADY_INITIALIZED = 5
    NVML_ERROR_NOT_FOUND = 6
    NVML_ERROR_INSUFFICIENT_SIZE = 7
    NVML_ERROR_INSUFFICIENT_POWER = 8
    NVML_ERROR_DRIVER_NOT_LOADED = 9
    NVML_ERROR_TIMEOUT = 10
    NVML_ERROR_IRQ_ISSUE = 11
    NVML_ERROR_LIBRARY_NOT_FOUND = 12
    NVML_ERROR_FUNCTION_NOT_FOUND = 13
    NVML_ERROR_CORRUPTED_INFOROM = 14
    NVML_ERROR_GPU_IS_LOST = 15
    NVML_ERROR_RESET_REQUIRED = 16
    NVML_ERROR_OPERATING_SYSTEM = 17
    NVML_ERROR_LIB_RM_VERSION_MISMATCH = 18
    NVML_ERROR_IN_USE = 19
    NVML_ERROR_MEMORY = 20
    NVML_ERROR_NO_DATA = 21
    NVML_ERROR_VGPU_ECC_NOT_SUPPORTED = 22
    NVML_ERROR_UNKNOWN = 999


_nvmlFanState_t = c_uint
NVML_FAN_NORMAL = 0
NVML_FAN_FAILED = 1
class nvmlFanState(Enum):
    """
    NVML_FAN_NORMAL       = 0,     //!< Fan is working properly
    NVML_FAN_FAILED       = 1      //!< Fan has failed
    """
    NVML_FAN_NORMAL = 0
    NVML_FAN_FAILED = 1


_nvmlLedColor_t = c_uint
NVML_LED_COLOR_GREEN = 0
NVML_LED_COLOR_AMBER = 1
class nvmlLedColor(Enum):
    """
    NVML_LED_COLOR_GREEN       = 0,     //!< GREEN, indicates good health
    NVML_LED_COLOR_AMBER       = 1      //!< AMBER, indicates problem
    """
    NVML_LED_COLOR_GREEN = 0
    NVML_LED_COLOR_AMBER = 1


_nvmlGpuOperationMode_t = c_uint
NVML_GOM_ALL_ON = 0
NVML_GOM_COMPUTE = 1
NVML_GOM_LOW_DP = 2
class nvmlGpuOperationMode(Enum):
    """
    // Everything is enabled and running at full speed
    NVML_GOM_ALL_ON = 0
    // Designed for running only compute tasks. Graphics operations are not
    // allowed
    NVML_GOM_COMPUTE = 1
    // Designed for running graphics applications that don't require
    NVML_GOM_LOW_DP = 2
    """
    NVML_GOM_ALL_ON = 0
    NVML_GOM_COMPUTE = 1
    NVML_GOM_LOW_DP = 2


_nvmlPageRetirementCause_t = c_uint
NVML_PAGE_RETIREMENT_CAUSE_DOUBLE_BIT_ECC_ERROR = 0
NVML_PAGE_RETIREMENT_CAUSE_MULTIPLE_SINGLE_BIT_ECC_ERRORS = 1
NVML_PAGE_RETIREMENT_CAUSE_COUNT = 2
class nvmlPageRetirementCause_t(Enum):
    """
    // Page was retired due to multiple single bit ECC error
    NVML_PAGE_RETIREMENT_CAUSE_MULTIPLE_SINGLE_BIT_ECC_ERRORS = 0,
    // Page was retired due to double bit ECC error
    NVML_PAGE_RETIREMENT_CAUSE_DOUBLE_BIT_ECC_ERROR = 1,
    """
    NVML_PAGE_RETIREMENT_CAUSE_DOUBLE_BIT_ECC_ERROR = 0
    NVML_PAGE_RETIREMENT_CAUSE_MULTIPLE_SINGLE_BIT_ECC_ERRORS = 1
    NVML_PAGE_RETIREMENT_CAUSE_COUNT = 2

_nvmlRestrictedAPI_t = c_uint
NVML_RESTRICTED_API_SET_APPLICATION_CLOCKS = 0
NVML_RESTRICTED_API_SET_AUTO_BOOSTED_CLOCKS = 1
NVML_RESTRICTED_API_COUNT = 2
class nvmlRestrictedAPI_t(Enum):
    """
    // APIs that change application clocks, see
    // nvmlDeviceSetApplicationsClocks and see
    // nvmlDeviceResetApplicationsClocks
    NVML_RESTRICTED_API_SET_APPLICATION_CLOCKS = 0,
    // APIs that enable/disable Auto Boosted clocks
    // see nvmlDeviceSetAutoBoostedClocksEnabled
    NVML_RESTRICTED_API_SET_AUTO_BOOSTED_CLOCKS = 1,
    """
    NVML_RESTRICTED_API_SET_APPLICATION_CLOCKS = 0
    NVML_RESTRICTED_API_SET_AUTO_BOOSTED_CLOCKS = 1
    NVML_RESTRICTED_API_COUNT = 2

_nvmlBridgeChipType_t = c_uint
NVML_BRIDGE_CHIP_PLX = 0
NVML_BRIDGE_CHIP_BRO4 = 1
NVML_MAX_PHYSICAL_BRIDGE = 128
class nvmlBridgeChipType_t(Enum):
    NVML_BRIDGE_CHIP_PLX = 0
    NVML_BRIDGE_CHIP_BRO4 = 1
    NVML_MAX_PHYSICAL_BRIDGE = 128

_nvmlValueType_t = c_uint
NVML_VALUE_TYPE_DOUBLE = 0
NVML_VALUE_TYPE_UNSIGNED_INT = 1
NVML_VALUE_TYPE_UNSIGNED_LONG = 2
NVML_VALUE_TYPE_UNSIGNED_LONG_LONG = 3
NVML_VALUE_TYPE_SIGNED_LONG_LONG = 4
NVML_VALUE_TYPE_COUNT = 5
class nvmlValueType_t(Enum):
    NVML_VALUE_TYPE_DOUBLE = 0
    NVML_VALUE_TYPE_UNSIGNED_INT = 1
    NVML_VALUE_TYPE_UNSIGNED_LONG = 2
    NVML_VALUE_TYPE_UNSIGNED_LONG_LONG = 3
    NVML_VALUE_TYPE_SIGNED_LONG_LONG = 4
    NVML_VALUE_TYPE_COUNT = 5

_nvmlPerfPolicyType_t = c_uint
NVML_PERF_POLICY_POWER = 0
NVML_PERF_POLICY_THERMAL = 1
NVML_PERF_POLICY_SYNC_BOOST = 2
NVML_PERF_POLICY_BOARD_LIMIT = 3
NVML_PERF_POLICY_LOW_UTILIZATION = 4
NVML_PERF_POLICY_RELIABILITY = 5
NVML_PERF_POLICY_TOTAL_APP_CLOCKS = 10
NVML_PERF_POLICY_TOTAL_BASE_CLOCKS = 11
NVML_PERF_POLICY_COUNT = 12
class nvmlPerfPolicyType_t(Enum):
    """
    // How long did power violations cause the GPU to be below application
    // clocks
    NVML_PERF_POLICY_POWER = 0,
    // How long did thermal violations cause the GPU to be below application
    // clocks
    NVML_PERF_POLICY_THERMAL = 1,
    // How long did sync boost cause the GPU to be below application clocks
    NVML_PERF_POLICY_SYNC_BOOST = 2,
    // How long did the board limit cause the GPU to be below application clocks
    NVML_PERF_POLICY_BOARD_LIMIT = 3,
    // How long did low utilization cause the GPU to be below application clocks
    NVML_PERF_POLICY_LOW_UTILIZATION = 4,
    // How long did the board reliability limit cause the GPU to be below
    // application clocks
    NVML_PERF_POLICY_RELIABILITY = 5,
    // Total time the GPU was held below application clocks by any limiter
    // (0 - 5 above)
    NVML_PERF_POLICY_TOTAL_APP_CLOCKS = 10,
    // Total time the GPU was held below base clocks
    NVML_PERF_POLICY_TOTAL_BASE_CLOCKS = 11,
    """
    NVML_PERF_POLICY_POWER = 0
    NVML_PERF_POLICY_THERMAL = 1
    NVML_PERF_POLICY_SYNC_BOOST = 2
    NVML_PERF_POLICY_BOARD_LIMIT = 3
    NVML_PERF_POLICY_LOW_UTILIZATION = 4
    NVML_PERF_POLICY_RELIABILITY = 5
    NVML_PERF_POLICY_TOTAL_APP_CLOCKS = 10
    NVML_PERF_POLICY_TOTAL_BASE_CLOCKS = 11
    NVML_PERF_POLICY_COUNT = 12

_nvmlSamplingType_t = c_uint
NVML_TOTAL_POWER_SAMPLES = 0
NVML_GPU_UTILIZATION_SAMPLES = 1
NVML_MEMORY_UTILIZATION_SAMPLES = 2
NVML_ENC_UTILIZATION_SAMPLES = 3
NVML_DEC_UTILIZATION_SAMPLES = 4
NVML_PROCESSOR_CLK_SAMPLES = 5
NVML_MEMORY_CLK_SAMPLES = 6
NVML_SAMPLINGTYPE_COUNT = 7
class nvmlSamplingType_t(Enum):
    """
    // To represent total power drawn by GPU
    NVML_TOTAL_POWER_SAMPLES        = 0,
    // To represent percent of time during which one or more kernels was
    // executing on the GPU
    NVML_GPU_UTILIZATION_SAMPLES    = 1,
    // To represent percent of time during which global (device) memory was
    // being read or written
    NVML_MEMORY_UTILIZATION_SAMPLES = 2,
    // To represent percent of time during which NVENC remains busy
    NVML_ENC_UTILIZATION_SAMPLES    = 3,
    // To represent percent of time during which NVDEC remains busy
    NVML_DEC_UTILIZATION_SAMPLES    = 4,
    // To represent processor clock samples
    NVML_PROCESSOR_CLK_SAMPLES      = 5,
    // To represent memory clock samples
    NVML_MEMORY_CLK_SAMPLES         = 6,
    """
    NVML_TOTAL_POWER_SAMPLES = 0
    NVML_GPU_UTILIZATION_SAMPLES = 1
    NVML_MEMORY_UTILIZATION_SAMPLES = 2
    NVML_ENC_UTILIZATION_SAMPLES = 3
    NVML_DEC_UTILIZATION_SAMPLES = 4
    NVML_PROCESSOR_CLK_SAMPLES = 5
    NVML_MEMORY_CLK_SAMPLES = 6
    NVML_SAMPLINGTYPE_COUNT = 7

_nvmlPcieUtilCounter_t = c_uint
NVML_PCIE_UTIL_TX_BYTES = 0
NVML_PCIE_UTIL_RX_BYTES = 1
NVML_PCIE_UTIL_COUNT = 2
class nvmlPcieUtilCouter_t(Enum):
    """
    NVML_PCIE_UTIL_TX_BYTES             = 0, // 1KB granularity
    NVML_PCIE_UTIL_RX_BYTES             = 1, // 1KB granularity
    """
    NVML_PCIE_UTIL_TX_BYTES = 0
    NVML_PCIE_UTIL_RX_BYTES = 1
    NVML_PCIE_UTIL_COUNT = 2

_nvmlGpuTopologyLevel_t = c_uint
NVML_TOPOLOGY_INTERNAL = 0
NVML_TOPOLOGY_SINGLE = 10
NVML_TOPOLOGY_MULTIPLE = 20
NVML_TOPOLOGY_HOSTBRIDGE = 30
NVML_TOPOLOGY_CPU = 40
NVML_TOPOLOGY_SYSTEM = 50
class nvmlGpuTopologyLevel_t(Enum):
    """
    // e.g. Tesla K80
    NVML_TOPOLOGY_INTERNAL           = 0,
    // all devices that only need traverse a single PCIe switch
    NVML_TOPOLOGY_SINGLE             = 10,
    // all devices that need not traverse a host bridge
    NVML_TOPOLOGY_MULTIPLE           = 20,
    // all devices that are connected to the same host bridge
    NVML_TOPOLOGY_HOSTBRIDGE         = 30,
    // all devices that are connected to the same NUMA node but possibly
    // multiple host bridges
    NVML_TOPOLOGY_NODE               = 40,
    // all devices in the system
    NVML_TOPOLOGY_SYSTEM             = 50,
    """
    NVML_TOPOLOGY_INTERNAL = 0
    NVML_TOPOLOGY_SINGLE = 10
    NVML_TOPOLOGY_MULTIPLE = 20
    NVML_TOPOLOGY_HOSTBRIDGE = 30
    NVML_TOPOLOGY_CPU = 40
    NVML_TOPOLOGY_SYSTEM = 50


# C preprocessor defined values
nvmlFlagDefault = 0
nvmlFlagForce = 1

# buffer size
NVML_DEVICE_INFOROM_VERSION_BUFFER_SIZE = 16
NVML_DEVICE_UUID_BUFFER_SIZE = 80
NVML_SYSTEM_DRIVER_VERSION_BUFFER_SIZE = 81
NVML_SYSTEM_NVML_VERSION_BUFFER_SIZE = 80
NVML_DEVICE_NAME_BUFFER_SIZE = 64
NVML_DEVICE_SERIAL_BUFFER_SIZE = 30
NVML_DEVICE_VBIOS_VERSION_BUFFER_SIZE = 32
NVML_DEVICE_PCI_BUS_ID_BUFFER_SIZE = 16

NVML_VALUE_NOT_AVAILABLE_ulonglong = c_ulonglong(-1)
NVML_VALUE_NOT_AVAILABLE_uint = c_uint(-1)

# Lib loading #
nvmlLib = None
libLoadLock = threading.Lock()
# Incremented on each nvmlInit and decremented on nvmlShutdown
_nvmlLib_refcount = 0


# Error Checking #
class NVMLError(Exception):
    _valClassMapping = dict()
    # List of currently known error codes
    _errcode_to_string = {
        NVML_ERROR_UNINITIALIZED:       "Uninitialized",
        NVML_ERROR_INVALID_ARGUMENT:    "Invalid Argument",
        NVML_ERROR_NOT_SUPPORTED:       "Not Supported",
        NVML_ERROR_NO_PERMISSION:       "Insufficient Permissions",
        NVML_ERROR_ALREADY_INITIALIZED: "Already Initialized",
        NVML_ERROR_NOT_FOUND:           "Not Found",
        NVML_ERROR_INSUFFICIENT_SIZE:   "Insufficient Size",
        NVML_ERROR_INSUFFICIENT_POWER:  "Insufficient External Power",
        NVML_ERROR_DRIVER_NOT_LOADED:   "Driver Not Loaded",
        NVML_ERROR_TIMEOUT:             "Timeout",
        NVML_ERROR_IRQ_ISSUE:           "Interrupt Request Issue",
        NVML_ERROR_LIBRARY_NOT_FOUND:   "NVML Shared Library Not Found",
        NVML_ERROR_FUNCTION_NOT_FOUND:  "Function Not Found",
        NVML_ERROR_CORRUPTED_INFOROM:   "Corrupted infoROM",
        NVML_ERROR_GPU_IS_LOST:         "GPU is lost",
        NVML_ERROR_RESET_REQUIRED:      "GPU requires restart",
        NVML_ERROR_OPERATING_SYSTEM:    "The operating system has blocked the request.",
        NVML_ERROR_LIB_RM_VERSION_MISMATCH: "RM has detected an NVML/RM version mismatch.",
        NVML_ERROR_IN_USE:              "The GPU is currently in use",
        NVML_ERROR_MEMORY:              "Insufficient Memory",
        NVML_ERROR_NO_DATA:             "No data",
        NVML_ERROR_VGPU_ECC_NOT_SUPPORTED: "Requested vgpu operation not available with ECC enabled",
        NVML_ERROR_UNKNOWN:             "Unknown Error",
        }
    def __new__(typ, value):
        """
        Maps value to a proper subclass of NVMLError.
        See _extractNVMLErrorsAsClasses function for more details
        """
        if typ == NVMLError:
            typ = NVMLError._valClassMapping.get(value, typ)
        obj = Exception.__new__(typ)
        obj.value = value
        return obj

    def __str__(self):
        try:
            if self.value not in NVMLError._errcode_to_string:
                NVMLError._errcode_to_string[self.value] = str(nvmlErrorString(self.value))
            return NVMLError._errcode_to_string[self.value]
        except KeyError:
            return "NVML Error with code %d" % self.value

    def __eq__(self, other):
        return self.value == other.value


def _extractNVMLErrorsAsClasses():
    """
    Generates a hierarchy of classes on top of NVMLError class.

    Each NVML Error gets a new NVMLError subclass. This way try,except blocks
    can filter appropriate exceptions more easily.

    NVMLError is a parent class. Each NVML_ERROR_* gets it's own subclass.  e.g.
    NVML_ERROR_ALREADY_INITIALIZED will be turned into
    NVMLError_AlreadyInitialized
    """
    this_module = sys.modules[__name__]
    nvmlErrorsNames = [x for x in dir(this_module) if x.startswith("NVML_ERROR_")]
    for err_name in nvmlErrorsNames:
        # e.g. Turn NVML_ERROR_ALREADY_INITIALIZED into NVMLError_AlreadyInitialized
        class_name = "NVMLError_" + string.capwords(err_name.replace("NVML_ERROR_", ""), "_").replace("_", "")
        err_val = getattr(this_module, err_name)
        def gen_new(val):
            def new(typ):
                obj = NVMLError.__new__(typ, val)
                return obj
            return new
        new_error_class = type(class_name, (NVMLError,), {'__new__': gen_new(err_val)})
        new_error_class.__module__ = __name__
        setattr(this_module, class_name, new_error_class)
        NVMLError._valClassMapping[err_val] = new_error_class


_extractNVMLErrorsAsClasses()


def _nvmlCheckReturn(ret):
    if (ret != NVML_SUCCESS):
        raise NVMLError(ret)
    return ret


# Function access
# function pointers are cached to prevent unnecessary libLoadLock locking
_nvmlGetFunctionPointer_cache = dict()
def _nvmlGetFunctionPointer(name):
    global nvmlLib

    if name in _nvmlGetFunctionPointer_cache:
        return _nvmlGetFunctionPointer_cache[name]

    libLoadLock.acquire()
    try:
        # ensure library was loaded
        if (nvmlLib is None):
            raise NVMLError(NVML_ERROR_UNINITIALIZED)
        try:
            _nvmlGetFunctionPointer_cache[name] = getattr(nvmlLib, name)
            return _nvmlGetFunctionPointer_cache[name]
        except AttributeError:
            raise NVMLError(NVML_ERROR_FUNCTION_NOT_FOUND)
    finally:
        # lock is always freed
        libLoadLock.release()


# # Alternative object
# Allows the object to be printed
# Allows mismatched types to be assigned
#  - like None when the Structure variant requires c_uint
class nvmlFriendlyObject(object):
    def __init__(self, dictionary):
        for x in dictionary:
            setattr(self, x, dictionary[x])

    def __str__(self):
        return self.__dict__.__str__()


def nvmlStructToFriendlyObject(struct):
    d = {}
    for x in struct._fields_:
        key = x[0]
        value = getattr(struct, key)
        d[key] = value
    obj = nvmlFriendlyObject(d)
    return obj


# pack the object so it can be passed to the NVML library
def nvmlFriendlyObjectToStruct(obj, model):
    for x in model._fields_:
        key = x[0]
        value = obj.__dict__[key]
        setattr(model, key, value)
    return model


# Unit structures
class struct_c_nvmlUnit_t(Structure):
    pass  # opaque handle
c_nvmlUnit_t = POINTER(struct_c_nvmlUnit_t)


# Convert bytes objects to strings or leave untouched
def bytes_to_str(s):
    if type(s) is bytes:
        try:
            return str(s, 'utf-8')
        except TypeError:  # Can get this if running python 2
            return str(s)
    else:
        return s


class _PrintableStructure(Structure):
    """
    Abstract class that produces nicer __str__ output than ctypes.Structure.
    e.g. instead of:
      >>> print str(obj)
      <class_name object at 0x7fdf82fef9e0>
    this class will print
      class_name(field_name: formatted_value, field_name: formatted_value)

    _fmt_ dictionary of <str _field_ name> -> <str format>
    e.g. class that has _field_ 'hex_value', c_uint could be formatted with
      _fmt_ = {"hex_value" : "%08X"}
    to produce nicer output.
    Default fomratting string for all fields can be set with key "<default>" like:
      _fmt_ = {"<default>" : "%d MHz"} # e.g all values are numbers in MHz.
    If not set it's assumed to be just "%s"

    Exact format of returned str from this class is subject to change in the future.
    """
    _fmt_ = {}
    def __str__(self):
        result = []
        for x in self._fields_:
            key = x[0]
            value = getattr(self, key)
            fmt = "%s"
            if key in self._fmt_:
                fmt = self._fmt_[key]
            elif "<default>" in self._fmt_:
                fmt = self._fmt_["<default>"]
            result.append(("%s: " + fmt) % (key, value))
        return self.__class__.__name__ + "(" + ", ".join(result) + ")"


class c_nvmlUnitInfo_t(_PrintableStructure):
    _fields_ = [
        ('name', c_char * 96),
        ('id', c_char * 96),
        ('serial', c_char * 96),
        ('firmwareVersion', c_char * 96),
    ]


class c_nvmlLedState_t(_PrintableStructure):
    _fields_ = [
        ('cause', c_char * 256),
        ('color', _nvmlLedColor_t),
    ]


class c_nvmlPSUInfo_t(_PrintableStructure):
    _fields_ = [
        ('state', c_char * 256),
        ('current', c_uint),
        ('voltage', c_uint),
        ('power', c_uint),
    ]


class c_nvmlUnitFanInfo_t(_PrintableStructure):
    _fields_ = [
        ('speed', c_uint),
        ('state', _nvmlFanState_t),
    ]


class c_nvmlUnitFanSpeeds_t(_PrintableStructure):
    _fields_ = [
        ('fans', c_nvmlUnitFanInfo_t * 24),
        ('count', c_uint)
    ]


# Device structures
class struct_c_nvmlDevice_t(Structure):
    pass # opaque handle
c_nvmlDevice_t = POINTER(struct_c_nvmlDevice_t)


class nvmlPciInfo_t(_PrintableStructure):
    _fields_ = [
        ('busId', c_char * 16),
        ('domain', c_uint),
        ('bus', c_uint),
        ('device', c_uint),
        ('pciDeviceId', c_uint),

        # Added in 2.285
        ('pciSubSystemId', c_uint),
        ('reserved0', c_uint),
        ('reserved1', c_uint),
        ('reserved2', c_uint),
        ('reserved3', c_uint),
    ]
    _fmt_ = {
            'domain'         : "0x%04X",
            'bus'            : "0x%02X",
            'device'         : "0x%02X",
            'pciDeviceId'    : "0x%08X",
            'pciSubSystemId' : "0x%08X",
            }


class c_nvmlMemory_t(_PrintableStructure):
    _fields_ = [
        ('total', c_ulonglong),
        ('free', c_ulonglong),
        ('used', c_ulonglong),
    ]
    _fmt_ = {'<default>': "%d B"}


class c_nvmlBAR1Memory_t(_PrintableStructure):
    _fields_ = [
        ('bar1Total', c_ulonglong),
        ('bar1Free', c_ulonglong),
        ('bar1Used', c_ulonglong),
    ]
    _fmt_ = {'<default>': "%d B"}


# On Windows with the WDDM driver, usedGpuMemory is reported as None
# Code that processes this structure should check for None, I.E.
#
# if (info.usedGpuMemory == None):
#     # TODO handle the error
#     pass
# else:
#    print("Using %d MiB of memory" % (info.usedGpuMemory / 1024 / 1024))
#
# See NVML documentation for more information
class c_nvmlProcessInfo_t(_PrintableStructure):
    _fields_ = [
        ('pid', c_uint),
        ('usedGpuMemory', c_ulonglong),
    ]
    _fmt_ = {'usedGpuMemory': "%d B"}


class c_nvmlBridgeChipInfo_t(_PrintableStructure):
    _fields_ = [
        ('type', _nvmlBridgeChipType_t),
        ('fwVersion', c_uint),
    ]


class c_nvmlBridgeChipHierarchy_t(_PrintableStructure):
    _fields_ = [
        ('bridgeCount', c_uint),
        ('bridgeChipInfo', c_nvmlBridgeChipInfo_t * 128),
    ]


class c_nvmlEccErrorCounts_t(_PrintableStructure):
    _fields_ = [
        ('l1Cache', c_ulonglong),
        ('l2Cache', c_ulonglong),
        ('deviceMemory', c_ulonglong),
        ('registerFile', c_ulonglong),
    ]


class c_nvmlUtilization_t(_PrintableStructure):
    _fields_ = [
        ('gpu', c_uint),
        ('memory', c_uint),
    ]
    _fmt_ = {'<default>': "%d %%"}


# Added in 2.285
class c_nvmlHwbcEntry_t(_PrintableStructure):
    _fields_ = [
        ('hwbcId', c_uint),
        ('firmwareVersion', c_char * 32),
    ]


class c_nvmlValue_t(Union):
    _fields_ = [
        ('dVal', c_double),
        ('uiVal', c_uint),
        ('ulVal', c_ulong),
        ('ullVal', c_ulonglong),
    ]


class c_nvmlSample_t(_PrintableStructure):
    _fields_ = [
        ('timeStamp', c_ulonglong),
        ('sampleValue', c_nvmlValue_t),
    ]


class c_nvmlViolationTime_t(_PrintableStructure):
    _fields_ = [
        ('referenceTime', c_ulonglong),
        ('violationTime', c_ulonglong),
    ]


# Event structures
class struct_c_nvmlEventSet_t(Structure):
    pass # opaque handle


c_nvmlEventSet_t = POINTER(struct_c_nvmlEventSet_t)
nvmlEventTypeSingleBitEccError     = 0x0000000000000001
nvmlEventTypeDoubleBitEccError     = 0x0000000000000002
nvmlEventTypePState                = 0x0000000000000004
nvmlEventTypeXidCriticalError      = 0x0000000000000008
nvmlEventTypeClock                 = 0x0000000000000010
nvmlEventTypeNone                  = 0x0000000000000000
nvmlEventTypeAll                   = (
                                        nvmlEventTypeNone |
                                        nvmlEventTypeSingleBitEccError |
                                        nvmlEventTypeDoubleBitEccError |
                                        nvmlEventTypePState |
                                        nvmlEventTypeClock |
                                        nvmlEventTypeXidCriticalError
                                     )

## Clock Throttle Reasons defines
nvmlClocksThrottleReasonGpuIdle           = 0x0000000000000001
nvmlClocksThrottleReasonApplicationsClocksSetting = 0x0000000000000002
nvmlClocksThrottleReasonUserDefinedClocks         = nvmlClocksThrottleReasonApplicationsClocksSetting # deprecated, use nvmlClocksThrottleReasonApplicationsClocksSetting
nvmlClocksThrottleReasonSwPowerCap        = 0x0000000000000004
nvmlClocksThrottleReasonHwSlowdown        = 0x0000000000000008
nvmlClocksThrottleReasonUnknown           = 0x8000000000000000
nvmlClocksThrottleReasonNone              = 0x0000000000000000
nvmlClocksThrottleReasonAll               = (
                                               nvmlClocksThrottleReasonNone |
                                               nvmlClocksThrottleReasonGpuIdle |
                                               nvmlClocksThrottleReasonApplicationsClocksSetting |
                                               nvmlClocksThrottleReasonSwPowerCap |
                                               nvmlClocksThrottleReasonHwSlowdown |
                                               nvmlClocksThrottleReasonUnknown
                                            )

class c_nvmlEventData_t(_PrintableStructure):
    _fields_ = [
        ('device', c_nvmlDevice_t),
        ('eventType', c_ulonglong),
        ('eventData', c_ulonglong)
    ]
    _fmt_ = {'eventType': "0x%08X"}

class c_nvmlAccountingStats_t(_PrintableStructure):
    _fields_ = [
        ('gpuUtilization', c_uint),
        ('memoryUtilization', c_uint),
        ('maxMemoryUsage', c_ulonglong),
        ('time', c_ulonglong),
        ('startTime', c_ulonglong),
        ('isRunning', c_uint),
        ('reserved', c_uint * 5)
    ]

## C function wrappers ##
def nvmlInit():
    r"""
    /**
     * Initialize NVML, but don't initialize any GPUs yet.
     *
     * \note nvmlInit_v3 introduces a "flags" argument, that allows passing boolean values
     *       modifying the behaviour of nvmlInit().
     * \note In NVML 5.319 new nvmlInit_v2 has replaced nvmlInit"_v1" (default in NVML 4.304 and older) that
     *       did initialize all GPU devices in the system.
     *
     * This allows NVML to communicate with a GPU
     * when other GPUs in the system are unstable or in a bad state.  When using this API, GPUs are
     * discovered and initialized in nvmlDeviceGetHandleBy* functions instead.
     *
     * \note To contrast nvmlInit_v2 with nvmlInit"_v1", NVML 4.304 nvmlInit"_v1" will fail when any detected GPU is in
     *       a bad or unstable state.
     *
     * For all products.
     *
     * This method, should be called once before invoking any other methods in the library.
     * A reference count of the number of initializations is maintained.  Shutdown only occurs
     * when the reference count reaches zero.
     *
     * @return
     *         - \ref NVML_SUCCESS                   if NVML has been properly initialized
     *         - \ref NVML_ERROR_DRIVER_NOT_LOADED   if NVIDIA driver is not running
     *         - \ref NVML_ERROR_NO_PERMISSION       if NVML does not have permission to talk to the driver
     *         - \ref NVML_ERROR_UNKNOWN             on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlInit
    """
    _LoadNvmlLibrary()

    #
    # Initialize the library
    #
    fn = _nvmlGetFunctionPointer("nvmlInit_v2")
    ret = fn()
    _nvmlCheckReturn(ret)

    # Atomically update refcount
    global _nvmlLib_refcount
    libLoadLock.acquire()
    _nvmlLib_refcount += 1
    libLoadLock.release()
    global nvmlLib
    return nvmlLib


def _LoadNvmlLibrary():
    """
    Load the library if it isn't loaded already
    """
    global nvmlLib

    if (nvmlLib is None):
        # lock to ensure only one caller loads the library
        libLoadLock.acquire()

        try:
            # ensure the library still isn't loaded
            if (nvmlLib is None):
                try:
                    if (sys.platform[:3] == "win"):
                        searchPaths = [
                            os.path.join(os.getenv("ProgramFiles", r"C:\Program Files"), r"NVIDIA Corporation\NVSMI\nvml.dll"),
                            os.path.join(os.getenv("WinDir", r"C:\Windows"), r"System32\nvml.dll"),
                        ]
                        nvmlPath = next((x for x in searchPaths if os.path.isfile(x)), None)
                        if (nvmlPath == None):
                            _nvmlCheckReturn(NVML_ERROR_LIBRARY_NOT_FOUND)
                        else:
                            # cdecl calling convention
                            nvmlLib = CDLL(nvmlPath)
                    else:
                        # assume linux
                        nvmlLib = CDLL("libnvidia-ml.so.1")
                except OSError as ose:
                    _nvmlCheckReturn(NVML_ERROR_LIBRARY_NOT_FOUND)
                if (nvmlLib == None):
                    _nvmlCheckReturn(NVML_ERROR_LIBRARY_NOT_FOUND)
        finally:
            # lock is always freed
            libLoadLock.release()


def nvmlShutdown():
    r"""
    /**
     * Shut down NVML by releasing all GPU resources previously allocated with \ref nvmlInit().
     *
     * For all products.
     *
     * This method should be called after NVML work is done, once for each call to \ref nvmlInit()
     * A reference count of the number of initializations is maintained.  Shutdown only occurs
     * when the reference count reaches zero.  For backwards compatibility, no error is reported if
     * nvmlShutdown() is called more times than nvmlInit().
     *
     * @return
     *         - \ref NVML_SUCCESS                 if NVML has been properly shut down
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlShutdown
    """
    #
    # Leave the library loaded, but shutdown the interface
    #
    fn = _nvmlGetFunctionPointer("nvmlShutdown")
    ret = fn()
    _nvmlCheckReturn(ret)

    # Atomically update refcount
    global _nvmlLib_refcount
    libLoadLock.acquire()
    if (0 < _nvmlLib_refcount):
        _nvmlLib_refcount -= 1
    libLoadLock.release()
    return None

# Added in 2.285
def nvmlErrorString(result):
    fn = _nvmlGetFunctionPointer("nvmlErrorString")
    fn.restype = c_char_p # otherwise return is an int
    ret = fn(result)
    return bytes_to_str(ret)

# Added in 2.285
def nvmlSystemGetNVMLVersion():
    r"""
    /**
     * Retrieves the version of the NVML library.
     *
     * For all products.
     *
     * The version identifier is an alphanumeric string.  It will not exceed 80 characters in length
     * (including the NULL terminator).  See \ref nvmlConstants::NVML_SYSTEM_NVML_VERSION_BUFFER_SIZE.
     *
     * @param version                              Reference in which to return the version identifier
     * @param length                               The maximum allowed length of the string returned in \a version
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a version has been set
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a version is NULL
     *         - \ref NVML_ERROR_INSUFFICIENT_SIZE if \a length is too small
     */
    nvmlReturn_t DECLDIR nvmlSystemGetNVMLVersion
    """
    c_version = create_string_buffer(NVML_SYSTEM_NVML_VERSION_BUFFER_SIZE)
    fn = _nvmlGetFunctionPointer("nvmlSystemGetNVMLVersion")
    ret = fn(c_version, c_uint(NVML_SYSTEM_NVML_VERSION_BUFFER_SIZE))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_version.value)

# Added in 2.285
def nvmlSystemGetProcessName(pid):
    r"""
    /**
     * Gets name of the process with provided process id
     *
     * For all products.
     *
     * Returned process name is cropped to provided length.
     * name string is encoded in ANSI.
     *
     * @param pid                                  The identifier of the process
     * @param name                                 Reference in which to return the process name
     * @param length                               The maximum allowed length of the string returned in \a name
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a name has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a name is NULL or \a length is 0.
     *         - \ref NVML_ERROR_NOT_FOUND         if process doesn't exists
     *         - \ref NVML_ERROR_NO_PERMISSION     if the user doesn't have permission to perform this operation
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlSystemGetProcessName
    """
    c_name = create_string_buffer(1024)
    fn = _nvmlGetFunctionPointer("nvmlSystemGetProcessName")
    ret = fn(c_uint(pid), c_name, c_uint(1024))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_name.value)

def nvmlSystemGetDriverVersion():
    r"""
    /**
     * Retrieves the version of the system's graphics driver.
     *
     * For all products.
     *
     * The version identifier is an alphanumeric string.  It will not exceed 80 characters in length
     * (including the NULL terminator).  See \ref nvmlConstants::NVML_SYSTEM_DRIVER_VERSION_BUFFER_SIZE.
     *
     * @param version                              Reference in which to return the version identifier
     * @param length                               The maximum allowed length of the string returned in \a version
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a version has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a version is NULL
     *         - \ref NVML_ERROR_INSUFFICIENT_SIZE if \a length is too small
     */
    nvmlReturn_t DECLDIR nvmlSystemGetDriverVersion
    """
    c_version = create_string_buffer(NVML_SYSTEM_DRIVER_VERSION_BUFFER_SIZE)
    fn = _nvmlGetFunctionPointer("nvmlSystemGetDriverVersion")
    ret = fn(c_version, c_uint(NVML_SYSTEM_DRIVER_VERSION_BUFFER_SIZE))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_version.value)

# Added in 2.285
def nvmlSystemGetHicVersion():
    r"""
    /**
     * Retrieves the IDs and firmware versions for any Host Interface Cards (HICs) in the system.
     *
     * For S-class products.
     *
     * The \a hwbcCount argument is expected to be set to the size of the input \a hwbcEntries array.
     * The HIC must be connected to an S-class system for it to be reported by this function.
     *
     * @param hwbcCount                            Size of hwbcEntries array
     * @param hwbcEntries                          Array holding information about hwbc
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a hwbcCount and \a hwbcEntries have been populated
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if either \a hwbcCount or \a hwbcEntries is NULL
     *         - \ref NVML_ERROR_INSUFFICIENT_SIZE if \a hwbcCount indicates that the \a hwbcEntries array is too small
     */
    nvmlReturn_t DECLDIR nvmlSystemGetHicVersion
    """
    c_count = c_uint(0)
    hics = None
    fn = _nvmlGetFunctionPointer("nvmlSystemGetHicVersion")

    # get the count
    ret = fn(byref(c_count), None)

    # this should only fail with insufficient size
    if ((ret != NVML_SUCCESS) and
        (ret != NVML_ERROR_INSUFFICIENT_SIZE)):
        raise NVMLError(ret)

    # if there are no hics
    if (c_count.value == 0):
        return []

    hic_array = c_nvmlHwbcEntry_t * c_count.value
    hics = hic_array()
    ret = fn(byref(c_count), hics)
    _nvmlCheckReturn(ret)
    return bytes_to_str(hics)


## Unit get functions
def nvmlUnitGetCount():
    r"""
    /**
     * Retrieves the number of units in the system.
     *
     * For S-class products.
     *
     * @param unitCount                            Reference in which to return the number of units
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a unitCount has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a unitCount is NULL
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlUnitGetCount
    """
    """
/**
 * Retrieves the number of units in the system.
 *
 * For S-class products.
 *
 * @param unitCount                            Reference in which to return the number of units
 *
 * @return
 *         - \ref NVML_SUCCESS                 if \a unitCount has been set
 *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
 *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a unitCount is NULL
 *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
 */
    """
    c_count = c_uint()
    fn = _nvmlGetFunctionPointer("nvmlUnitGetCount")
    ret = fn(byref(c_count))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_count.value)

def nvmlUnitGetHandleByIndex(index):
    r"""
    /**
     * Acquire the handle for a particular unit, based on its index.
     *
     * For S-class products.
     *
     * Valid indices are derived from the \a unitCount returned by \ref nvmlUnitGetCount().
     *   For example, if \a unitCount is 2 the valid indices are 0 and 1, corresponding to UNIT 0 and UNIT 1.
     *
     * The order in which NVML enumerates units has no guarantees of consistency between reboots.
     *
     * @param index                                The index of the target unit, >= 0 and < \a unitCount
     * @param unit                                 Reference in which to return the unit handle
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a unit has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a index is invalid or \a unit is NULL
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlUnitGetHandleByIndex
    """
    """
/**
 * Acquire the handle for a particular unit, based on its index.
 *
 * For S-class products.
 *
 * Valid indices are derived from the \a unitCount returned by \ref nvmlUnitGetCount().
 *   For example, if \a unitCount is 2 the valid indices are 0 and 1, corresponding to UNIT 0 and UNIT 1.
 *
 * The order in which NVML enumerates units has no guarantees of consistency between reboots.
 *
 * @param index                                The index of the target unit, >= 0 and < \a unitCount
 * @param unit                                 Reference in which to return the unit handle
 *
 * @return
 *         - \ref NVML_SUCCESS                 if \a unit has been set
 *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
 *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a index is invalid or \a unit is NULL
 *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
 */
    """
    c_index = c_uint(index)
    unit = c_nvmlUnit_t()
    fn = _nvmlGetFunctionPointer("nvmlUnitGetHandleByIndex")
    ret = fn(c_index, byref(unit))
    _nvmlCheckReturn(ret)
    return bytes_to_str(unit)

def nvmlUnitGetUnitInfo(unit):
    r"""
    /**
     * Retrieves the static information associated with a unit.
     *
     * For S-class products.
     *
     * See \ref nvmlUnitInfo_t for details on available unit info.
     *
     * @param unit                                 The identifier of the target unit
     * @param info                                 Reference in which to return the unit information
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a info has been populated
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a unit is invalid or \a info is NULL
     */
    nvmlReturn_t DECLDIR nvmlUnitGetUnitInfo
    """
    """
/**
 * Retrieves the static information associated with a unit.
 *
 * For S-class products.
 *
 * See \ref nvmlUnitInfo_t for details on available unit info.
 *
 * @param unit                                 The identifier of the target unit
 * @param info                                 Reference in which to return the unit information
 *
 * @return
 *         - \ref NVML_SUCCESS                 if \a info has been populated
 *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
 *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a unit is invalid or \a info is NULL
 */
    """
    c_info = c_nvmlUnitInfo_t()
    fn = _nvmlGetFunctionPointer("nvmlUnitGetUnitInfo")
    ret = fn(unit, byref(c_info))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_info)

def nvmlUnitGetLedState(unit):
    r"""
    /**
     * Retrieves the LED state associated with this unit.
     *
     * For S-class products.
     *
     * See \ref nvmlLedState_t for details on allowed states.
     *
     * @param unit                                 The identifier of the target unit
     * @param state                                Reference in which to return the current LED state
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a state has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a unit is invalid or \a state is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if this is not an S-class product
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     *
     * @see nvmlUnitSetLedState()
     */
    nvmlReturn_t DECLDIR nvmlUnitGetLedState
    """
    """
/**
 * Retrieves the LED state associated with this unit.
 *
 * For S-class products.
 *
 * See \ref nvmlLedState_t for details on allowed states.
 *
 * @param unit                                 The identifier of the target unit
 * @param state                                Reference in which to return the current LED state
 *
 * @return
 *         - \ref NVML_SUCCESS                 if \a state has been set
 *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
 *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a unit is invalid or \a state is NULL
 *         - \ref NVML_ERROR_NOT_SUPPORTED     if this is not an S-class product
 *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
 *
 * @see nvmlUnitSetLedState()
 */
    """
    c_state =  c_nvmlLedState_t()
    fn = _nvmlGetFunctionPointer("nvmlUnitGetLedState")
    ret = fn(unit, byref(c_state))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_state)

def nvmlUnitGetPsuInfo(unit):
    r"""
    /**
     * Retrieves the PSU stats for the unit.
     *
     * For S-class products.
     *
     * See \ref nvmlPSUInfo_t for details on available PSU info.
     *
     * @param unit                                 The identifier of the target unit
     * @param psu                                  Reference in which to return the PSU information
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a psu has been populated
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a unit is invalid or \a psu is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if this is not an S-class product
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlUnitGetPsuInfo
    """
    """
/**
 * Retrieves the PSU stats for the unit.
 *
 * For S-class products.
 *
 * See \ref nvmlPSUInfo_t for details on available PSU info.
 *
 * @param unit                                 The identifier of the target unit
 * @param psu                                  Reference in which to return the PSU information
 *
 * @return
 *         - \ref NVML_SUCCESS                 if \a psu has been populated
 *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
 *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a unit is invalid or \a psu is NULL
 *         - \ref NVML_ERROR_NOT_SUPPORTED     if this is not an S-class product
 *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
 */
    """
    c_info = c_nvmlPSUInfo_t()
    fn = _nvmlGetFunctionPointer("nvmlUnitGetPsuInfo")
    ret = fn(unit, byref(c_info))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_info)

def nvmlUnitGetTemperature(unit, type):
    r"""
    /**
     * Retrieves the temperature readings for the unit, in degrees C.
     *
     * For S-class products.
     *
     * Depending on the product, readings may be available for intake (type=0),
     * exhaust (type=1) and board (type=2).
     *
     * @param unit                                 The identifier of the target unit
     * @param type                                 The type of reading to take
     * @param temp                                 Reference in which to return the intake temperature
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a temp has been populated
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a unit or \a type is invalid or \a temp is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if this is not an S-class product
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlUnitGetTemperature
    """
    """
/**
 * Retrieves the temperature readings for the unit, in degrees C.
 *
 * For S-class products.
 *
 * Depending on the product, readings may be available for intake (type=0),
 * exhaust (type=1) and board (type=2).
 *
 * @param unit                                 The identifier of the target unit
 * @param type                                 The type of reading to take
 * @param temp                                 Reference in which to return the intake temperature
 *
 * @return
 *         - \ref NVML_SUCCESS                 if \a temp has been populated
 *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
 *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a unit or \a type is invalid or \a temp is NULL
 *         - \ref NVML_ERROR_NOT_SUPPORTED     if this is not an S-class product
 *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
 */
    """
    c_temp = c_uint()
    fn = _nvmlGetFunctionPointer("nvmlUnitGetTemperature")
    ret = fn(unit, c_uint(type), byref(c_temp))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_temp.value)

def nvmlUnitGetFanSpeedInfo(unit):
    r"""
    /**
     * Retrieves the fan speed readings for the unit.
     *
     * For S-class products.
     *
     * See \ref nvmlUnitFanSpeeds_t for details on available fan speed info.
     *
     * @param unit                                 The identifier of the target unit
     * @param fanSpeeds                            Reference in which to return the fan speed information
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a fanSpeeds has been populated
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a unit is invalid or \a fanSpeeds is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if this is not an S-class product
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlUnitGetFanSpeedInfo
    """
    """
/**
 * Retrieves the fan speed readings for the unit.
 *
 * For S-class products.
 *
 * See \ref nvmlUnitFanSpeeds_t for details on available fan speed info.
 *
 * @param unit                                 The identifier of the target unit
 * @param fanSpeeds                            Reference in which to return the fan speed information
 *
 * @return
 *         - \ref NVML_SUCCESS                 if \a fanSpeeds has been populated
 *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
 *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a unit is invalid or \a fanSpeeds is NULL
 *         - \ref NVML_ERROR_NOT_SUPPORTED     if this is not an S-class product
 *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
 */
    """
    c_speeds = c_nvmlUnitFanSpeeds_t()
    fn = _nvmlGetFunctionPointer("nvmlUnitGetFanSpeedInfo")
    ret = fn(unit, byref(c_speeds))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_speeds)

# added to API
def nvmlUnitGetDeviceCount(unit):
    """
    """
    c_count = c_uint(0)
    # query the unit to determine device count
    fn = _nvmlGetFunctionPointer("nvmlUnitGetDevices")
    ret = fn(unit, byref(c_count), None)
    if (ret == NVML_ERROR_INSUFFICIENT_SIZE):
        ret = NVML_SUCCESS
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_count.value)

def nvmlUnitGetDevices(unit):
    r"""
    /**
     * Retrieves the set of GPU devices that are attached to the specified unit.
     *
     * For S-class products.
     *
     * The \a deviceCount argument is expected to be set to the size of the input \a devices array.
     *
     * @param unit                                 The identifier of the target unit
     * @param deviceCount                          Reference in which to provide the \a devices array size, and
     *                                             to return the number of attached GPU devices
     * @param devices                              Reference in which to return the references to the attached GPU devices
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a deviceCount and \a devices have been populated
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INSUFFICIENT_SIZE if \a deviceCount indicates that the \a devices array is too small
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a unit is invalid, either of \a deviceCount or \a devices is NULL
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlUnitGetDevices
    """
    """
/**
 * Retrieves the set of GPU devices that are attached to the specified unit.
 *
 * For S-class products.
 *
 * The \a deviceCount argument is expected to be set to the size of the input \a devices array.
 *
 * @param unit                                 The identifier of the target unit
 * @param deviceCount                          Reference in which to provide the \a devices array size, and
 *                                             to return the number of attached GPU devices
 * @param devices                              Reference in which to return the references to the attached GPU devices
 *
 * @return
 *         - \ref NVML_SUCCESS                 if \a deviceCount and \a devices have been populated
 *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
 *         - \ref NVML_ERROR_INSUFFICIENT_SIZE if \a deviceCount indicates that the \a devices array is too small
 *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a unit is invalid, either of \a deviceCount or \a devices is NULL
 *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
 */
    """
    c_count = c_uint(nvmlUnitGetDeviceCount(unit))
    device_array = c_nvmlDevice_t * c_count.value
    c_devices = device_array()
    fn = _nvmlGetFunctionPointer("nvmlUnitGetDevices")
    ret = fn(unit, byref(c_count), c_devices)
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_devices)

## Device get functions
def nvmlDeviceGetCount():
    r"""
    /**
     * Retrieves the number of compute devices in the system. A compute device is a single GPU.
     *
     * For all products.
     *
     * Note: New nvmlDeviceGetCount_v2 (default in NVML 5.319) returns count of all devices in the system
     *       even if nvmlDeviceGetHandleByIndex_v2 returns NVML_ERROR_NO_PERMISSION for such device.
     *       Update your code to handle this error, or use NVML 4.304 or older nvml header file.
     *       For backward binary compatibility reasons _v1 version of the API is still present in the shared
     *       library.
     *       Old _v1 version of nvmlDeviceGetCount doesn't count devices that NVML has no permission to talk to.
     *
     * @param deviceCount                          Reference in which to return the number of accessible devices
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a deviceCount has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a deviceCount is NULL
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetCount
    """
    """
 /**
 * Retrieves the number of compute devices in the system. A compute device is a single GPU.
 *
 * For all products.
 *
 * Note: New nvmlDeviceGetCount_v2 (default in NVML 5.319) returns count of all devices in the system
 *       even if nvmlDeviceGetHandleByIndex_v2 returns NVML_ERROR_NO_PERMISSION for such device.
 *       Update your code to handle this error, or use NVML 4.304 or older nvml header file.
 *       For backward binary compatibility reasons _v1 version of the API is still present in the shared
 *       library.
 *       Old _v1 version of nvmlDeviceGetCount doesn't count devices that NVML has no permission to talk to.
 *
 * @param deviceCount                          Reference in which to return the number of accessible devices
 *
 * @return
 *         - \ref NVML_SUCCESS                 if \a deviceCount has been set
 *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
 *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a deviceCount is NULL
 *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
 */
    """
    c_count = c_uint()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetCount_v2")
    ret = fn(byref(c_count))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_count.value)

def nvmlDeviceGetHandleByIndex(index):
    r"""
    /**
     * Acquire the handle for a particular device, based on its index.
     *
     * For all products.
     *
     * Valid indices are derived from the \a accessibleDevices count returned by
     *   \ref nvmlDeviceGetCount(). For example, if \a accessibleDevices is 2 the valid indices
     *   are 0 and 1, corresponding to GPU 0 and GPU 1.
     *
     * The order in which NVML enumerates devices has no guarantees of consistency between reboots. For that reason it
     *   is recommended that devices be looked up by their PCI ids or UUID. See
     *   \ref nvmlDeviceGetHandleByUUID() and \ref nvmlDeviceGetHandleByPciBusId().
     *
     * Note: The NVML index may not correlate with other APIs, such as the CUDA device index.
     *
     * Starting from NVML 5, this API causes NVML to initialize the target GPU
     * NVML may initialize additional GPUs if:
     *  - The target GPU is an SLI slave
     *
     * Note: New nvmlDeviceGetCount_v2 (default in NVML 5.319) returns count of all devices in the system
     *       even if nvmlDeviceGetHandleByIndex_v2 returns NVML_ERROR_NO_PERMISSION for such device.
     *       Update your code to handle this error, or use NVML 4.304 or older nvml header file.
     *       For backward binary compatibility reasons _v1 version of the API is still present in the shared
     *       library.
     *       Old _v1 version of nvmlDeviceGetCount doesn't count devices that NVML has no permission to talk to.
     *
     *       This means that nvmlDeviceGetHandleByIndex_v2 and _v1 can return different devices for the same index.
     *       If you don't touch macros that map old (_v1) versions to _v2 versions at the top of the file you don't
     *       need to worry about that.
     *
     * @param index                                The index of the target GPU, >= 0 and < \a accessibleDevices
     * @param device                               Reference in which to return the device handle
     *
     * @return
     *         - \ref NVML_SUCCESS                  if \a device has been set
     *         - \ref NVML_ERROR_UNINITIALIZED      if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT   if \a index is invalid or \a device is NULL
     *         - \ref NVML_ERROR_INSUFFICIENT_POWER if any attached devices have improperly attached external power cables
     *         - \ref NVML_ERROR_NO_PERMISSION      if the user doesn't have permission to talk to this device
     *         - \ref NVML_ERROR_IRQ_ISSUE          if NVIDIA kernel detected an interrupt issue with the attached GPUs
     *         - \ref NVML_ERROR_GPU_IS_LOST        if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN            on any unexpected error
     *
     * @see nvmlDeviceGetIndex
     * @see nvmlDeviceGetCount
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetHandleByIndex
    """
    """
/**
 * Acquire the handle for a particular device, based on its index.
 *
 * For all products.
 *
 * Valid indices are derived from the \a accessibleDevices count returned by
 *   \ref nvmlDeviceGetCount(). For example, if \a accessibleDevices is 2 the valid indices
 *   are 0 and 1, corresponding to GPU 0 and GPU 1.
 *
 * The order in which NVML enumerates devices has no guarantees of consistency between reboots. For that reason it
 *   is recommended that devices be looked up by their PCI ids or UUID. See
 *   \ref nvmlDeviceGetHandleByUUID() and \ref nvmlDeviceGetHandleByPciBusId().
 *
 * Note: The NVML index may not correlate with other APIs, such as the CUDA device index.
 *
 * Starting from NVML 5, this API causes NVML to initialize the target GPU
 * NVML may initialize additional GPUs if:
 *  - The target GPU is an SLI slave
 *
 * Note: New nvmlDeviceGetCount_v2 (default in NVML 5.319) returns count of all devices in the system
 *       even if nvmlDeviceGetHandleByIndex_v2 returns NVML_ERROR_NO_PERMISSION for such device.
 *       Update your code to handle this error, or use NVML 4.304 or older nvml header file.
 *       For backward binary compatibility reasons _v1 version of the API is still present in the shared
 *       library.
 *       Old _v1 version of nvmlDeviceGetCount doesn't count devices that NVML has no permission to talk to.
 *
 *       This means that nvmlDeviceGetHandleByIndex_v2 and _v1 can return different devices for the same index.
 *       If you don't touch macros that map old (_v1) versions to _v2 versions at the top of the file you don't
 *       need to worry about that.
 *
 * @param index                                The index of the target GPU, >= 0 and < \a accessibleDevices
 * @param device                               Reference in which to return the device handle
 *
 * @return
 *         - \ref NVML_SUCCESS                  if \a device has been set
 *         - \ref NVML_ERROR_UNINITIALIZED      if the library has not been successfully initialized
 *         - \ref NVML_ERROR_INVALID_ARGUMENT   if \a index is invalid or \a device is NULL
 *         - \ref NVML_ERROR_INSUFFICIENT_POWER if any attached devices have improperly attached external power cables
 *         - \ref NVML_ERROR_NO_PERMISSION      if the user doesn't have permission to talk to this device
 *         - \ref NVML_ERROR_IRQ_ISSUE          if NVIDIA kernel detected an interrupt issue with the attached GPUs
 *         - \ref NVML_ERROR_GPU_IS_LOST        if the target GPU has fallen off the bus or is otherwise inaccessible
 *         - \ref NVML_ERROR_UNKNOWN            on any unexpected error
 *
 * @see nvmlDeviceGetIndex
 * @see nvmlDeviceGetCount
 */
    """
    c_index = c_uint(index)
    device = c_nvmlDevice_t()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetHandleByIndex_v2")
    ret = fn(c_index, byref(device))
    _nvmlCheckReturn(ret)
    return bytes_to_str(device)

def nvmlDeviceGetHandleBySerial(serial):
    r"""
    /**
     * Acquire the handle for a particular device, based on its board serial number.
     *
     * For Fermi &tm; or newer fully supported devices.
     *
     * This number corresponds to the value printed directly on the board, and to the value returned by
     *   \ref nvmlDeviceGetSerial().
     *
     * @deprecated Since more than one GPU can exist on a single board this function is deprecated in favor
     *             of \ref nvmlDeviceGetHandleByUUID.
     *             For dual GPU boards this function will return NVML_ERROR_INVALID_ARGUMENT.
     *
     * Starting from NVML 5, this API causes NVML to initialize the target GPU
     * NVML may initialize additional GPUs as it searches for the target GPU
     *
     * @param serial                               The board serial number of the target GPU
     * @param device                               Reference in which to return the device handle
     *
     * @return
     *         - \ref NVML_SUCCESS                  if \a device has been set
     *         - \ref NVML_ERROR_UNINITIALIZED      if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT   if \a serial is invalid, \a device is NULL or more than one
     *                                              device has the same serial (dual GPU boards)
     *         - \ref NVML_ERROR_NOT_FOUND          if \a serial does not match a valid device on the system
     *         - \ref NVML_ERROR_INSUFFICIENT_POWER if any attached devices have improperly attached external power cables
     *         - \ref NVML_ERROR_IRQ_ISSUE          if NVIDIA kernel detected an interrupt issue with the attached GPUs
     *         - \ref NVML_ERROR_GPU_IS_LOST        if any GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN            on any unexpected error
     *
     * @see nvmlDeviceGetSerial
     * @see nvmlDeviceGetHandleByUUID
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetHandleBySerial
    """
    """
/**
 * Acquire the handle for a particular device, based on its board serial number.
 *
 * For Fermi &tm; or newer fully supported devices.
 *
 * This number corresponds to the value printed directly on the board, and to the value returned by
 *   \ref nvmlDeviceGetSerial().
 *
 * @deprecated Since more than one GPU can exist on a single board this function is deprecated in favor
 *             of \ref nvmlDeviceGetHandleByUUID.
 *             For dual GPU boards this function will return NVML_ERROR_INVALID_ARGUMENT.
 *
 * Starting from NVML 5, this API causes NVML to initialize the target GPU
 * NVML may initialize additional GPUs as it searches for the target GPU
 *
 * @param serial                               The board serial number of the target GPU
 * @param device                               Reference in which to return the device handle
 *
 * @return
 *         - \ref NVML_SUCCESS                  if \a device has been set
 *         - \ref NVML_ERROR_UNINITIALIZED      if the library has not been successfully initialized
 *         - \ref NVML_ERROR_INVALID_ARGUMENT   if \a serial is invalid, \a device is NULL or more than one
 *                                              device has the same serial (dual GPU boards)
 *         - \ref NVML_ERROR_NOT_FOUND          if \a serial does not match a valid device on the system
 *         - \ref NVML_ERROR_INSUFFICIENT_POWER if any attached devices have improperly attached external power cables
 *         - \ref NVML_ERROR_IRQ_ISSUE          if NVIDIA kernel detected an interrupt issue with the attached GPUs
 *         - \ref NVML_ERROR_GPU_IS_LOST        if any GPU has fallen off the bus or is otherwise inaccessible
 *         - \ref NVML_ERROR_UNKNOWN            on any unexpected error
 *
 * @see nvmlDeviceGetSerial
 * @see nvmlDeviceGetHandleByUUID
 */
    """
    c_serial = c_char_p(serial)
    device = c_nvmlDevice_t()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetHandleBySerial")
    ret = fn(c_serial, byref(device))
    _nvmlCheckReturn(ret)
    return bytes_to_str(device)

def nvmlDeviceGetHandleByUUID(uuid):
    r"""
    /**
     * Acquire the handle for a particular device, based on its globally unique immutable UUID associated with each device.
     *
     * For all products.
     *
     * @param uuid                                 The UUID of the target GPU
     * @param device                               Reference in which to return the device handle
     *
     * Starting from NVML 5, this API causes NVML to initialize the target GPU
     * NVML may initialize additional GPUs as it searches for the target GPU
     *
     * @return
     *         - \ref NVML_SUCCESS                  if \a device has been set
     *         - \ref NVML_ERROR_UNINITIALIZED      if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT   if \a uuid is invalid or \a device is null
     *         - \ref NVML_ERROR_NOT_FOUND          if \a uuid does not match a valid device on the system
     *         - \ref NVML_ERROR_INSUFFICIENT_POWER if any attached devices have improperly attached external power cables
     *         - \ref NVML_ERROR_IRQ_ISSUE          if NVIDIA kernel detected an interrupt issue with the attached GPUs
     *         - \ref NVML_ERROR_GPU_IS_LOST        if any GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN            on any unexpected error
     *
     * @see nvmlDeviceGetUUID
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetHandleByUUID
    """
    """
/**
 * Acquire the handle for a particular device, based on its globally unique immutable UUID associated with each device.
 *
 * For all products.
 *
 * @param uuid                                 The UUID of the target GPU
 * @param device                               Reference in which to return the device handle
 *
 * Starting from NVML 5, this API causes NVML to initialize the target GPU
 * NVML may initialize additional GPUs as it searches for the target GPU
 *
 * @return
 *         - \ref NVML_SUCCESS                  if \a device has been set
 *         - \ref NVML_ERROR_UNINITIALIZED      if the library has not been successfully initialized
 *         - \ref NVML_ERROR_INVALID_ARGUMENT   if \a uuid is invalid or \a device is null
 *         - \ref NVML_ERROR_NOT_FOUND          if \a uuid does not match a valid device on the system
 *         - \ref NVML_ERROR_INSUFFICIENT_POWER if any attached devices have improperly attached external power cables
 *         - \ref NVML_ERROR_IRQ_ISSUE          if NVIDIA kernel detected an interrupt issue with the attached GPUs
 *         - \ref NVML_ERROR_GPU_IS_LOST        if any GPU has fallen off the bus or is otherwise inaccessible
 *         - \ref NVML_ERROR_UNKNOWN            on any unexpected error
 *
 * @see nvmlDeviceGetUUID
 */
    """
    c_uuid = c_char_p(uuid)
    device = c_nvmlDevice_t()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetHandleByUUID")
    ret = fn(c_uuid, byref(device))
    _nvmlCheckReturn(ret)
    return bytes_to_str(device)

def nvmlDeviceGetHandleByPciBusId(pciBusId):
    r"""
    /**
     * Acquire the handle for a particular device, based on its PCI bus id.
     *
     * For all products.
     *
     * This value corresponds to the nvmlPciInfo_t::busId returned by \ref nvmlDeviceGetPciInfo().
     *
     * Starting from NVML 5, this API causes NVML to initialize the target GPU
     * NVML may initialize additional GPUs if:
     *  - The target GPU is an SLI slave
     *
     * \note NVML 4.304 and older version of nvmlDeviceGetHandleByPciBusId"_v1" returns NVML_ERROR_NOT_FOUND
     *       instead of NVML_ERROR_NO_PERMISSION.
     *
     * @param pciBusId                             The PCI bus id of the target GPU
     * @param device                               Reference in which to return the device handle
     *
     * @return
     *         - \ref NVML_SUCCESS                  if \a device has been set
     *         - \ref NVML_ERROR_UNINITIALIZED      if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT   if \a pciBusId is invalid or \a device is NULL
     *         - \ref NVML_ERROR_NOT_FOUND          if \a pciBusId does not match a valid device on the system
     *         - \ref NVML_ERROR_INSUFFICIENT_POWER if the attached device has improperly attached external power cables
     *         - \ref NVML_ERROR_NO_PERMISSION      if the user doesn't have permission to talk to this device
     *         - \ref NVML_ERROR_IRQ_ISSUE          if NVIDIA kernel detected an interrupt issue with the attached GPUs
     *         - \ref NVML_ERROR_GPU_IS_LOST        if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN            on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetHandleByPciBusId
    """
    """
/**
 * Acquire the handle for a particular device, based on its PCI bus id.
 *
 * For all products.
 *
 * This value corresponds to the nvmlPciInfo_t::busId returned by \ref nvmlDeviceGetPciInfo().
 *
 * Starting from NVML 5, this API causes NVML to initialize the target GPU
 * NVML may initialize additional GPUs if:
 *  - The target GPU is an SLI slave
 *
 * \note NVML 4.304 and older version of nvmlDeviceGetHandleByPciBusId"_v1" returns NVML_ERROR_NOT_FOUND
 *       instead of NVML_ERROR_NO_PERMISSION.
 *
 * @param pciBusId                             The PCI bus id of the target GPU
 * @param device                               Reference in which to return the device handle
 *
 * @return
 *         - \ref NVML_SUCCESS                  if \a device has been set
 *         - \ref NVML_ERROR_UNINITIALIZED      if the library has not been successfully initialized
 *         - \ref NVML_ERROR_INVALID_ARGUMENT   if \a pciBusId is invalid or \a device is NULL
 *         - \ref NVML_ERROR_NOT_FOUND          if \a pciBusId does not match a valid device on the system
 *         - \ref NVML_ERROR_INSUFFICIENT_POWER if the attached device has improperly attached external power cables
 *         - \ref NVML_ERROR_NO_PERMISSION      if the user doesn't have permission to talk to this device
 *         - \ref NVML_ERROR_IRQ_ISSUE          if NVIDIA kernel detected an interrupt issue with the attached GPUs
 *         - \ref NVML_ERROR_GPU_IS_LOST        if the target GPU has fallen off the bus or is otherwise inaccessible
 *         - \ref NVML_ERROR_UNKNOWN            on any unexpected error
 */
    """
    c_busId = c_char_p(pciBusId)
    device = c_nvmlDevice_t()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetHandleByPciBusId_v2")
    ret = fn(c_busId, byref(device))
    _nvmlCheckReturn(ret)
    return bytes_to_str(device)

def nvmlDeviceGetName(handle):
    r"""
    /**
     * Retrieves the name of this device.
     *
     * For all products.
     *
     * The name is an alphanumeric string that denotes a particular product, e.g. Tesla &tm; C2070. It will not
     * exceed 64 characters in length (including the NULL terminator).  See \ref
     * nvmlConstants::NVML_DEVICE_NAME_BUFFER_SIZE.
     *
     * @param device                               The identifier of the target device
     * @param name                                 Reference in which to return the product name
     * @param length                               The maximum allowed length of the string returned in \a name
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a name has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid, or \a name is NULL
     *         - \ref NVML_ERROR_INSUFFICIENT_SIZE if \a length is too small
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetName
    """
    c_name = create_string_buffer(NVML_DEVICE_NAME_BUFFER_SIZE)
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetName")
    ret = fn(handle, c_name, c_uint(NVML_DEVICE_NAME_BUFFER_SIZE))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_name.value)

def nvmlDeviceGetBoardId(handle):
    r"""
    /**
     * Retrieves the device boardId from 0-N.
     * Devices with the same boardId indicate GPUs connected to the same PLX.  Use in conjunction with
     *  \ref nvmlDeviceGetMultiGpuBoard() to decide if they are on the same board as well.
     *  The boardId returned is a unique ID for the current configuration.  Uniqueness and ordering across
     *  reboots and system configurations is not guaranteed (i.e. if a Tesla K40c returns 0x100 and
     *  the two GPUs on a Tesla K10 in the same system returns 0x200 it is not guaranteed they will
     *  always return those values but they will always be different from each other).
     *
     *
     * For Fermi &tm; or newer fully supported devices.
     *
     * @param device                               The identifier of the target device
     * @param boardId                              Reference in which to return the device's board ID
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a boardId has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or \a boardId is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not support this feature
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetBoardId
    """
    c_id = c_uint();
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetBoardId")
    ret = fn(handle, byref(c_id))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_id.value)

def nvmlDeviceGetMultiGpuBoard(handle):
    r"""
    /**
     * Retrieves whether the device is on a Multi-GPU Board
     * Devices that are on multi-GPU boards will set \a multiGpuBool to a non-zero value.
     *
     * For Fermi &tm; or newer fully supported devices.
     *
     * @param device                               The identifier of the target device
     * @param multiGpuBool                         Reference in which to return a zero or non-zero value
     *                                                 to indicate whether the device is on a multi GPU board
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a multiGpuBool has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or \a multiGpuBool is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not support this feature
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetMultiGpuBoard
    """
    c_multiGpu = c_uint();
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetMultiGpuBoard")
    ret = fn(handle, byref(c_multiGpu))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_multiGpu.value)

def nvmlDeviceGetBrand(handle):
    r"""
    /**
     * Retrieves the brand of this device.
     *
     * For all products.
     *
     * The type is a member of \ref nvmlBrandType_t defined above.
     *
     * @param device                               The identifier of the target device
     * @param type                                 Reference in which to return the product brand type
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a name has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid, or \a type is NULL
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetBrand
    """
    c_type = _nvmlBrandType_t()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetBrand")
    ret = fn(handle, byref(c_type))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_type.value)

def nvmlDeviceGetSerial(handle):
    r"""
    /**
     * Retrieves the globally unique board serial number associated with this device's board.
     *
     * For all products with an inforom.
     *
     * The serial number is an alphanumeric string that will not exceed 30 characters (including the NULL terminator).
     * This number matches the serial number tag that is physically attached to the board.  See \ref
     * nvmlConstants::NVML_DEVICE_SERIAL_BUFFER_SIZE.
     *
     * @param device                               The identifier of the target device
     * @param serial                               Reference in which to return the board/module serial number
     * @param length                               The maximum allowed length of the string returned in \a serial
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a serial has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid, or \a serial is NULL
     *         - \ref NVML_ERROR_INSUFFICIENT_SIZE if \a length is too small
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not support this feature
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetSerial
    """
    c_serial = create_string_buffer(NVML_DEVICE_SERIAL_BUFFER_SIZE)
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetSerial")
    ret = fn(handle, c_serial, c_uint(NVML_DEVICE_SERIAL_BUFFER_SIZE))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_serial.value)

def nvmlDeviceGetCpuAffinity(handle, cpuSetSize):
    r"""
    /**
     * Retrieves an array of unsigned ints (sized to cpuSetSize) of bitmasks with the ideal CPU affinity for the device
     * For example, if processors 0, 1, 32, and 33 are ideal for the device and cpuSetSize == 2,
     *     result[0] = 0x3, result[1] = 0x3
     *
     * For Kepler &tm; or newer fully supported devices.
     * Supported on Linux only.
     *
     * @param device                               The identifier of the target device
     * @param cpuSetSize                           The size of the cpuSet array that is safe to access
     * @param cpuSet                               Array reference in which to return a bitmask of CPUs, 64 CPUs per
     *                                                 unsigned long on 64-bit machines, 32 on 32-bit machines
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a cpuAffinity has been filled
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid, cpuSetSize == 0, or cpuSet is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not support this feature
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetCpuAffinity
    """
    affinity_array = c_ulonglong * cpuSetSize
    c_affinity = affinity_array()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetCpuAffinity")
    ret = fn(handle, cpuSetSize, byref(c_affinity))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_affinity)

def nvmlDeviceGetCudaComputeCapability(handle):
    r"""
    /**
     * Retrieves the CUDA compute capability of the device.
     *
     * For all products with an inforom.
     *
     * Returns the major and minor compute capability version numbers of the device. 
     * The major and minor versions are equivalent to the CU_DEVICE_ATTRIBUTE_COMPUTE_CAPABILITY_MINOR
     * and CU_DEVICE_ATTRIBUTE_COMPUTE_CAPABILITY_MAJOR attributes that would be returned by CUDA's cuDeviceGetAttribute().
     *
     * @param device                              The identifier of the target device
     * @param major                               Reference in which to return the major CUDA compute capability
     * @param minor                               Reference in which to return the minor CUDA compute capability
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a serial has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid, or \a serial is NULL
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetCudaComputeCapability
    """
    major = c_uint(0)
    minor = c_uint(0)
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetCudaComputeCapability")
    ret = fn(handle, byref(major), byref(minor))
    _nvmlCheckReturn(ret)
    return major.value + 0.1 * minor.value

def nvmlDeviceSetCpuAffinity(handle):
    r"""
    /**
     * Sets the ideal affinity for the calling thread and device using the guidelines
     * given in nvmlDeviceGetCpuAffinity().  Note, this is a change as of version 8.0.
     * Older versions set the affinity for a calling process and all children.
     * Currently supports up to 64 processors.
     *
     * For Kepler &tm; or newer fully supported devices.
     * Supported on Linux only.
     *
     * @param device                               The identifier of the target device
     *
     * @return
     *         - \ref NVML_SUCCESS                 if the calling process has been successfully bound
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not support this feature
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceSetCpuAffinity
    """
    fn = _nvmlGetFunctionPointer("nvmlDeviceSetCpuAffinity")
    ret = fn(handle)
    _nvmlCheckReturn(ret)
    return None

def nvmlDeviceClearCpuAffinity(handle):
    r"""
    /**
     * Clear all affinity bindings for the calling thread.  Note, this is a change as of version
     * 8.0 as older versions cleared the affinity for a calling process and all children.
     *
     * For Kepler &tm; or newer fully supported devices.
     * Supported on Linux only.
     *
     * @param device                               The identifier of the target device
     *
     * @return
     *         - \ref NVML_SUCCESS                 if the calling process has been successfully unbound
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceClearCpuAffinity
    """
    fn = _nvmlGetFunctionPointer("nvmlDeviceClearCpuAffinity")
    ret = fn(handle)
    _nvmlCheckReturn(ret)
    return None

def nvmlDeviceGetMinorNumber(handle):
    r"""
    /**
     * Retrieves minor number for the device. The minor number for the device is such that the Nvidia device node file for
     * each GPU will have the form /dev/nvidia[minor number].
     *
     * For all products.
     * Supported only for Linux
     *
     * @param device                                The identifier of the target device
     * @param minorNumber                           Reference in which to return the minor number for the device
     * @return
     *         - \ref NVML_SUCCESS                 if the minor number is successfully retrieved
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or \a minorNumber is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if this query is not supported by the device
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetMinorNumber
    """
    c_minor_number = c_uint()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetMinorNumber")
    ret = fn(handle, byref(c_minor_number))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_minor_number.value)

def nvmlDeviceGetUUID(handle):
    r"""
    /**
     * Retrieves the globally unique immutable UUID associated with this device, as a 5 part hexadecimal string,
     * that augments the immutable, board serial identifier.
     *
     * For all products.
     *
     * The UUID is a globally unique identifier. It is the only available identifier for pre-Fermi-architecture products.
     * It does NOT correspond to any identifier printed on the board.  It will not exceed 80 characters in length
     * (including the NULL terminator).  See \ref nvmlConstants::NVML_DEVICE_UUID_BUFFER_SIZE.
     *
     * @param device                               The identifier of the target device
     * @param uuid                                 Reference in which to return the GPU UUID
     * @param length                               The maximum allowed length of the string returned in \a uuid
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a uuid has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid, or \a uuid is NULL
     *         - \ref NVML_ERROR_INSUFFICIENT_SIZE if \a length is too small
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not support this feature
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetUUID
    """
    c_uuid = create_string_buffer(NVML_DEVICE_UUID_BUFFER_SIZE)
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetUUID")
    ret = fn(handle, c_uuid, c_uint(NVML_DEVICE_UUID_BUFFER_SIZE))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_uuid.value)

def nvmlDeviceGetInforomVersion(handle, infoRomObject):
    r"""
    /**
     * Retrieves the version information for the device's infoROM object.
     *
     * For all products with an inforom.
     *
     * Fermi and higher parts have non-volatile on-board memory for persisting device info, such as aggregate
     * ECC counts. The version of the data structures in this memory may change from time to time. It will not
     * exceed 16 characters in length (including the NULL terminator).
     * See \ref nvmlConstants::NVML_DEVICE_INFOROM_VERSION_BUFFER_SIZE.
     *
     * See \ref nvmlInforomObject_t for details on the available infoROM objects.
     *
     * @param device                               The identifier of the target device
     * @param object                               The target infoROM object
     * @param version                              Reference in which to return the infoROM version
     * @param length                               The maximum allowed length of the string returned in \a version
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a version has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a version is NULL
     *         - \ref NVML_ERROR_INSUFFICIENT_SIZE if \a length is too small
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not have an infoROM
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     *
     * @see nvmlDeviceGetInforomImageVersion
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetInforomVersion
    """
    c_version = create_string_buffer(NVML_DEVICE_INFOROM_VERSION_BUFFER_SIZE)
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetInforomVersion")
    ret = fn(handle, _nvmlInforomObject_t(infoRomObject),
	         c_version, c_uint(NVML_DEVICE_INFOROM_VERSION_BUFFER_SIZE))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_version.value)

# Added in 4.304
def nvmlDeviceGetInforomImageVersion(handle):
    r"""
    /**
     * Retrieves the global infoROM image version
     *
     * For all products with an inforom.
     *
     * Image version just like VBIOS version uniquely describes the exact version of the infoROM flashed on the board
     * in contrast to infoROM object version which is only an indicator of supported features.
     * Version string will not exceed 16 characters in length (including the NULL terminator).
     * See \ref nvmlConstants::NVML_DEVICE_INFOROM_VERSION_BUFFER_SIZE.
     *
     * @param device                               The identifier of the target device
     * @param version                              Reference in which to return the infoROM image version
     * @param length                               The maximum allowed length of the string returned in \a version
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a version has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a version is NULL
     *         - \ref NVML_ERROR_INSUFFICIENT_SIZE if \a length is too small
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not have an infoROM
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     *
     * @see nvmlDeviceGetInforomVersion
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetInforomImageVersion
    """
    c_version = create_string_buffer(NVML_DEVICE_INFOROM_VERSION_BUFFER_SIZE)
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetInforomImageVersion")
    ret = fn(handle, c_version, c_uint(NVML_DEVICE_INFOROM_VERSION_BUFFER_SIZE))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_version.value)

# Added in 4.304
def nvmlDeviceGetInforomConfigurationChecksum(handle):
    r"""
    /**
     * Retrieves the checksum of the configuration stored in the device's infoROM.
     *
     * For all products with an inforom.
     *
     * Can be used to make sure that two GPUs have the exact same configuration.
     * Current checksum takes into account configuration stored in PWR and ECC infoROM objects.
     * Checksum can change between driver releases or when user changes configuration (e.g. disable/enable ECC)
     *
     * @param device                               The identifier of the target device
     * @param checksum                             Reference in which to return the infoROM configuration checksum
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a checksum has been set
     *         - \ref NVML_ERROR_CORRUPTED_INFOROM if the device's checksum couldn't be retrieved due to infoROM corruption
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a checksum is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not support this feature
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetInforomConfigurationChecksum
    """
    c_checksum = c_uint()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetInforomConfigurationChecksum")
    ret = fn(handle, byref(c_checksum))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_checksum.value)

# Added in 4.304
def nvmlDeviceValidateInforom(handle):
    r"""
    /**
     * Reads the infoROM from the flash and verifies the checksums.
     *
     * For all products with an inforom.
     *
     * @param device                               The identifier of the target device
     *
     * @return
     *         - \ref NVML_SUCCESS                 if infoROM is not corrupted
     *         - \ref NVML_ERROR_CORRUPTED_INFOROM if the device's infoROM is corrupted
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not support this feature
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceValidateInforom
    """
    fn = _nvmlGetFunctionPointer("nvmlDeviceValidateInforom")
    ret = fn(handle)
    _nvmlCheckReturn(ret)
    return None

def nvmlDeviceGetDisplayMode(handle):
    r"""
    /**
     * Retrieves the display mode for the device.
     *
     * For all products.
     *
     * This method indicates whether a physical display (e.g. monitor) is currently connected to
     * any of the device's connectors.
     *
     * See \ref nvmlEnableState_t for details on allowed modes.
     *
     * @param device                               The identifier of the target device
     * @param display                              Reference in which to return the display mode
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a display has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or \a display is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not support this feature
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetDisplayMode
    """
    c_mode = _nvmlEnableState_t()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetDisplayMode")
    ret = fn(handle, byref(c_mode))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_mode.value)

def nvmlDeviceGetDisplayActive(handle):
    r"""
    /**
     * Retrieves the display active state for the device.
     *
     * For all products.
     *
     * This method indicates whether a display is initialized on the device.
     * For example whether X Server is attached to this device and has allocated memory for the screen.
     *
     * Display can be active even when no monitor is physically attached.
     *
     * See \ref nvmlEnableState_t for details on allowed modes.
     *
     * @param device                               The identifier of the target device
     * @param isActive                             Reference in which to return the display active state
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a isActive has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or \a isActive is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not support this feature
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetDisplayActive
    """
    c_mode = _nvmlEnableState_t()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetDisplayActive")
    ret = fn(handle, byref(c_mode))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_mode.value)


def nvmlDeviceGetPersistenceMode(handle):
    r"""
    /**
     * Retrieves the persistence mode associated with this device.
     *
     * For all products.
     * For Linux only.
     *
     * When driver persistence mode is enabled the driver software state is not torn down when the last
     * client disconnects. By default this feature is disabled.
     *
     * See \ref nvmlEnableState_t for details on allowed modes.
     *
     * @param device                               The identifier of the target device
     * @param mode                                 Reference in which to return the current driver persistence mode
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a mode has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or \a mode is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not support this feature
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     *
     * @see nvmlDeviceSetPersistenceMode()
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetPersistenceMode
    """
    c_state = _nvmlEnableState_t()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetPersistenceMode")
    ret = fn(handle, byref(c_state))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_state.value)

def nvmlDeviceGetPciInfo(handle):
    r"""
    /**
     * Retrieves the PCI attributes of this device.
     *
     * For all products.
     *
     * See \ref nvmlPciInfo_t for details on the available PCI info.
     *
     * @param device                               The identifier of the target device
     * @param pci                                  Reference in which to return the PCI info
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a pci has been populated
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or \a pci is NULL
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetPciInfo
    """
    c_info = nvmlPciInfo_t()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetPciInfo_v2")
    ret = fn(handle, byref(c_info))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_info)

def nvmlDeviceGetClockInfo(handle, type):
    r"""
    /**
     * Retrieves the current clock speeds for the device.
     *
     * For Fermi &tm; or newer fully supported devices.
     *
     * See \ref nvmlClockType_t for details on available clock information.
     *
     * @param device                               The identifier of the target device
     * @param type                                 Identify which clock domain to query
     * @param clock                                Reference in which to return the clock speed in MHz
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a clock has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or \a clock is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device cannot report the specified clock
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetClockInfo
    """
    c_clock = c_uint()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetClockInfo")
    ret = fn(handle, _nvmlClockType_t(type), byref(c_clock))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_clock.value)

# Added in 2.285
def nvmlDeviceGetMaxClockInfo(handle, type):
    r"""
    /**
     * Retrieves the maximum clock speeds for the device.
     *
     * For Fermi &tm; or newer fully supported devices.
     *
     * See \ref nvmlClockType_t for details on available clock information.
     *
     * \note On GPUs from Fermi family current P0 clocks (reported by \ref nvmlDeviceGetClockInfo) can differ from max clocks
     *       by few MHz.
     *
     * @param device                               The identifier of the target device
     * @param type                                 Identify which clock domain to query
     * @param clock                                Reference in which to return the clock speed in MHz
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a clock has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or \a clock is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device cannot report the specified clock
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetMaxClockInfo
    """
    c_clock = c_uint()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetMaxClockInfo")
    ret = fn(handle, _nvmlClockType_t(type), byref(c_clock))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_clock.value)

# Added in 4.304
def nvmlDeviceGetApplicationsClock(handle, type):
    r"""
    /**
     * Retrieves the current setting of a clock that applications will use unless an overspec situation occurs.
     * Can be changed using \ref nvmlDeviceSetApplicationsClocks.
     *
     * For Kepler &tm; or newer fully supported devices.
     *
     * @param device                               The identifier of the target device
     * @param clockType                            Identify which clock domain to query
     * @param clockMHz                             Reference in which to return the clock in MHz
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a clockMHz has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or \a clockMHz is NULL or \a clockType is invalid
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not support this feature
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetApplicationsClock
    """
    c_clock = c_uint()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetApplicationsClock")
    ret = fn(handle, _nvmlClockType_t(type), byref(c_clock))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_clock.value)

# Added in 5.319
def nvmlDeviceGetDefaultApplicationsClock(handle, type):
    r"""
    /**
     * Retrieves the default applications clock that GPU boots with or
     * defaults to after \ref nvmlDeviceResetApplicationsClocks call.
     *
     * For Kepler &tm; or newer fully supported devices.
     *
     * @param device                               The identifier of the target device
     * @param clockType                            Identify which clock domain to query
     * @param clockMHz                             Reference in which to return the default clock in MHz
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a clockMHz has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or \a clockMHz is NULL or \a clockType is invalid
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not support this feature
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     *
     * \see nvmlDeviceGetApplicationsClock
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetDefaultApplicationsClock
    """
    c_clock = c_uint()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetDefaultApplicationsClock")
    ret = fn(handle, _nvmlClockType_t(type), byref(c_clock))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_clock.value)

# Added in 4.304
def nvmlDeviceGetSupportedMemoryClocks(handle):
    r"""
    /**
     * Retrieves the list of possible memory clocks that can be used as an argument for \ref nvmlDeviceSetApplicationsClocks.
     *
     * For Kepler &tm; or newer fully supported devices.
     *
     * @param device                               The identifier of the target device
     * @param count                                Reference in which to provide the \a clocksMHz array size, and
     *                                             to return the number of elements
     * @param clocksMHz                            Reference in which to return the clock in MHz
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a count and \a clocksMHz have been populated
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or \a count is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not support this feature
     *         - \ref NVML_ERROR_INSUFFICIENT_SIZE if \a count is too small (\a count is set to the number of
     *                                                required elements)
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     *
     * @see nvmlDeviceSetApplicationsClocks
     * @see nvmlDeviceGetSupportedGraphicsClocks
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetSupportedMemoryClocks
    """
    # first call to get the size
    c_count = c_uint(0)
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetSupportedMemoryClocks")
    ret = fn(handle, byref(c_count), None)

    if (ret == NVML_SUCCESS):
        # special case, no clocks
        return []
    elif (ret == NVML_ERROR_INSUFFICIENT_SIZE):
        # typical case
        clocks_array = c_uint * c_count.value
        c_clocks = clocks_array()

        # make the call again
        ret = fn(handle, byref(c_count), c_clocks)
        _nvmlCheckReturn(ret)

        procs = []
        for i in range(c_count.value):
            procs.append(c_clocks[i])

        return procs
    else:
        # error case
        raise NVMLError(ret)

# Added in 4.304
def nvmlDeviceGetSupportedGraphicsClocks(handle, memoryClockMHz):
    r"""
    /**
     * Retrieves the list of possible graphics clocks that can be used as an argument for \ref nvmlDeviceSetApplicationsClocks.
     *
     * For Kepler &tm; or newer fully supported devices.
     *
     * @param device                               The identifier of the target device
     * @param memoryClockMHz                       Memory clock for which to return possible graphics clocks
     * @param count                                Reference in which to provide the \a clocksMHz array size, and
     *                                             to return the number of elements
     * @param clocksMHz                            Reference in which to return the clocks in MHz
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a count and \a clocksMHz have been populated
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_NOT_FOUND         if the specified \a memoryClockMHz is not a supported frequency
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or \a clock is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not support this feature
     *         - \ref NVML_ERROR_INSUFFICIENT_SIZE if \a count is too small
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     *
     * @see nvmlDeviceSetApplicationsClocks
     * @see nvmlDeviceGetSupportedMemoryClocks
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetSupportedGraphicsClocks
    """
    # first call to get the size
    c_count = c_uint(0)
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetSupportedGraphicsClocks")
    ret = fn(handle, c_uint(memoryClockMHz), byref(c_count), None)

    if (ret == NVML_SUCCESS):
        # special case, no clocks
        return []
    elif (ret == NVML_ERROR_INSUFFICIENT_SIZE):
        # typical case
        clocks_array = c_uint * c_count.value
        c_clocks = clocks_array()

        # make the call again
        ret = fn(handle, c_uint(memoryClockMHz), byref(c_count), c_clocks)
        _nvmlCheckReturn(ret)

        procs = []
        for i in range(c_count.value):
            procs.append(c_clocks[i])

        return procs
    else:
        # error case
        raise NVMLError(ret)

def nvmlDeviceGetFanSpeed(handle):
    r"""
    /**
     * Retrieves the intended operating speed of the device's fan.
     *
     * Note: The reported speed is the intended fan speed.  If the fan is physically blocked and unable to spin, the
     * output will not match the actual fan speed.
     *
     * For all discrete products with dedicated fans.
     *
     * The fan speed is expressed as a percent of the maximum, i.e. full speed is 100%.
     *
     * @param device                               The identifier of the target device
     * @param speed                                Reference in which to return the fan speed percentage
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a speed has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or \a speed is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not have a fan
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetFanSpeed
    """
    c_speed = c_uint()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetFanSpeed")
    ret = fn(handle, byref(c_speed))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_speed.value)

def nvmlDeviceGetTemperature(handle, sensor):
    r"""
    /**
     * Retrieves the current temperature readings for the device, in degrees C.
     *
     * For all products.
     *
     * See \ref nvmlTemperatureSensors_t for details on available temperature sensors.
     *
     * @param device                               The identifier of the target device
     * @param sensorType                           Flag that indicates which sensor reading to retrieve
     * @param temp                                 Reference in which to return the temperature reading
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a temp has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid, \a sensorType is invalid or \a temp is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not have the specified sensor
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetTemperature
    """
    c_temp = c_uint()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetTemperature")
    ret = fn(handle, _nvmlTemperatureSensors_t(sensor), byref(c_temp))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_temp.value)

def nvmlDeviceGetTemperatureThreshold(handle, threshold):
    r"""
    /**
     * Retrieves the temperature threshold for the GPU with the specified threshold type in degrees C.
     *
     * For Kepler &tm; or newer fully supported devices.
     *
     * See \ref nvmlTemperatureThresholds_t for details on available temperature thresholds.
     *
     * @param device                               The identifier of the target device
     * @param thresholdType                        The type of threshold value queried
     * @param temp                                 Reference in which to return the temperature reading
     * @return
     *         - \ref NVML_SUCCESS                 if \a temp has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid, \a thresholdType is invalid or \a temp is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not have a temperature sensor or is unsupported
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetTemperatureThreshold
    """
    c_temp = c_uint()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetTemperatureThreshold")
    ret = fn(handle, _nvmlTemperatureThresholds_t(threshold), byref(c_temp))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_temp.value)

# DEPRECATED use nvmlDeviceGetPerformanceState
def nvmlDeviceGetPowerState(handle):
    r"""
    /**
     * Deprecated: Use \ref nvmlDeviceGetPerformanceState. This function exposes an incorrect generalization.
     *
     * Retrieve the current performance state for the device.
     *
     * For Fermi &tm; or newer fully supported devices.
     *
     * See \ref nvmlPstates_t for details on allowed performance states.
     *
     * @param device                               The identifier of the target device
     * @param pState                               Reference in which to return the performance state reading
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a pState has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or \a pState is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not support this feature
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetPowerState
    """
    c_pstate = _nvmlPstates_t()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetPowerState")
    ret = fn(handle, byref(c_pstate))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_pstate.value)

def nvmlDeviceGetPerformanceState(handle):
    r"""
    /**
     * Retrieves the current performance state for the device.
     *
     * For Fermi &tm; or newer fully supported devices.
     *
     * See \ref nvmlPstates_t for details on allowed performance states.
     *
     * @param device                               The identifier of the target device
     * @param pState                               Reference in which to return the performance state reading
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a pState has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or \a pState is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not support this feature
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetPerformanceState
    """
    c_pstate = _nvmlPstates_t()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetPerformanceState")
    ret = fn(handle, byref(c_pstate))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_pstate.value)

def nvmlDeviceGetPowerManagementMode(handle):
    r"""
    /**
     * This API has been deprecated.
     *
     * Retrieves the power management mode associated with this device.
     *
     * For products from the Fermi family.
     *     - Requires \a NVML_INFOROM_POWER version 3.0 or higher.
     *
     * For from the Kepler or newer families.
     *     - Does not require \a NVML_INFOROM_POWER object.
     *
     * This flag indicates whether any power management algorithm is currently active on the device. An
     * enabled state does not necessarily mean the device is being actively throttled -- only that
     * that the driver will do so if the appropriate conditions are met.
     *
     * See \ref nvmlEnableState_t for details on allowed modes.
     *
     * @param device                               The identifier of the target device
     * @param mode                                 Reference in which to return the current power management mode
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a mode has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or \a mode is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not support this feature
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetPowerManagementMode
    """
    c_pcapMode = _nvmlEnableState_t()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetPowerManagementMode")
    ret = fn(handle, byref(c_pcapMode))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_pcapMode.value)

def nvmlDeviceGetPowerManagementLimit(handle):
    r"""
    /**
     * Retrieves the power management limit associated with this device.
     *
     * For Fermi &tm; or newer fully supported devices.
     *
     * The power limit defines the upper boundary for the card's power draw. If
     * the card's total power draw reaches this limit the power management algorithm kicks in.
     *
     * This reading is only available if power management mode is supported.
     * See \ref nvmlDeviceGetPowerManagementMode.
     *
     * @param device                               The identifier of the target device
     * @param limit                                Reference in which to return the power management limit in milliwatts
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a limit has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or \a limit is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not support this feature
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetPowerManagementLimit
    """
    c_limit = c_uint()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetPowerManagementLimit")
    ret = fn(handle, byref(c_limit))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_limit.value)

# Added in 4.304
def nvmlDeviceGetPowerManagementLimitConstraints(handle):
    r"""
    /**
     * Retrieves information about possible values of power management limits on this device.
     *
     * For Kepler &tm; or newer fully supported devices.
     *
     * @param device                               The identifier of the target device
     * @param minLimit                             Reference in which to return the minimum power management limit in milliwatts
     * @param maxLimit                             Reference in which to return the maximum power management limit in milliwatts
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a minLimit and \a maxLimit have been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or \a minLimit or \a maxLimit is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not support this feature
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     *
     * @see nvmlDeviceSetPowerManagementLimit
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetPowerManagementLimitConstraints
    """
    c_minLimit = c_uint()
    c_maxLimit = c_uint()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetPowerManagementLimitConstraints")
    ret = fn(handle, byref(c_minLimit), byref(c_maxLimit))
    _nvmlCheckReturn(ret)
    return [c_minLimit.value, c_maxLimit.value]

# Added in 4.304
def nvmlDeviceGetPowerManagementDefaultLimit(handle):
    r"""
    /**
     * Retrieves default power management limit on this device, in milliwatts.
     * Default power management limit is a power management limit that the device boots with.
     *
     * For Kepler &tm; or newer fully supported devices.
     *
     * @param device                               The identifier of the target device
     * @param defaultLimit                         Reference in which to return the default power management limit in milliwatts
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a defaultLimit has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or \a defaultLimit is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not support this feature
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetPowerManagementDefaultLimit
    """
    c_limit = c_uint()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetPowerManagementDefaultLimit")
    ret = fn(handle, byref(c_limit))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_limit.value)


# Added in 331
def nvmlDeviceGetEnforcedPowerLimit(handle):
    r"""
    /**
     * Get the effective power limit that the driver enforces after taking into account all limiters
     *
     * Note: This can be different from the \ref nvmlDeviceGetPowerManagementLimit if other limits are set elsewhere
     * This includes the out of band power limit interface
     *
     * For Kepler &tm; or newer fully supported devices.
     *
     * @param device                           The device to communicate with
     * @param limit                            Reference in which to return the power management limit in milliwatts
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a limit has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or \a limit is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not support this feature
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetEnforcedPowerLimit
    """
    c_limit = c_uint()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetEnforcedPowerLimit")
    ret = fn(handle, byref(c_limit))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_limit.value)

def nvmlDeviceGetPowerUsage(handle):
    r"""
    /**
     * Retrieves power usage for this GPU in milliwatts and its associated circuitry (e.g. memory)
     *
     * For Fermi &tm; or newer fully supported devices.
     *
     * On Fermi and Kepler GPUs the reading is accurate to within +/- 5% of current power draw.
     *
     * It is only available if power management mode is supported. See \ref nvmlDeviceGetPowerManagementMode.
     *
     * @param device                               The identifier of the target device
     * @param power                                Reference in which to return the power usage information
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a power has been populated
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or \a power is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not support power readings
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetPowerUsage
    """
    c_watts = c_uint()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetPowerUsage")
    ret = fn(handle, byref(c_watts))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_watts.value)

# Added in 4.304
def nvmlDeviceGetGpuOperationMode(handle):
    r"""
    /**
     * Retrieves the current GOM and pending GOM (the one that GPU will switch to after reboot).
     *
     * For GK110 M-class and X-class Tesla &tm; products from the Kepler family.
     * Modes \ref NVML_GOM_LOW_DP and \ref NVML_GOM_ALL_ON are supported on fully supported GeForce products.
     * Not supported on Quadro &reg; and Tesla &tm; C-class products.
     *
     * @param device                               The identifier of the target device
     * @param current                              Reference in which to return the current GOM
     * @param pending                              Reference in which to return the pending GOM
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a mode has been populated
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or \a current or \a pending is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not support this feature
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     *
     * @see nvmlGpuOperationMode_t
     * @see nvmlDeviceSetGpuOperationMode
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetGpuOperationMode
    """
    c_currState = _nvmlGpuOperationMode_t()
    c_pendingState = _nvmlGpuOperationMode_t()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetGpuOperationMode")
    ret = fn(handle, byref(c_currState), byref(c_pendingState))
    _nvmlCheckReturn(ret)
    return [c_currState.value, c_pendingState.value]

# Added in 4.304
def nvmlDeviceGetCurrentGpuOperationMode(handle):
    return nvmlDeviceGetGpuOperationMode(handle)[0]

# Added in 4.304
def nvmlDeviceGetPendingGpuOperationMode(handle):
    return nvmlDeviceGetGpuOperationMode(handle)[1]

def nvmlDeviceGetMemoryInfo(handle):
    r"""
    /**
     * Retrieves the amount of used, free and total memory available on the device, in bytes.
     *
     * For all products.
     *
     * Enabling ECC reduces the amount of total available memory, due to the extra required parity bits.
     * Under WDDM most device memory is allocated and managed on startup by Windows.
     *
     * Under Linux and Windows TCC, the reported amount of used memory is equal to the sum of memory allocated
     * by all active channels on the device.
     *
     * See \ref nvmlMemory_t for details on available memory info.
     *
     * @param device                               The identifier of the target device
     * @param memory                               Reference in which to return the memory information
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a memory has been populated
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or \a memory is NULL
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetMemoryInfo
    """
    c_memory = c_nvmlMemory_t()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetMemoryInfo")
    ret = fn(handle, byref(c_memory))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_memory)

def nvmlDeviceGetBAR1MemoryInfo(handle):
    r"""
    /**
     * Gets Total, Available and Used size of BAR1 memory.
     *
     * BAR1 is used to map the FB (device memory) so that it can be directly accessed by the CPU or by 3rd party
     * devices (peer-to-peer on the PCIE bus).
     *
     * For Kepler &tm; or newer fully supported devices.
     *
     * @param device                               The identifier of the target device
     * @param bar1Memory                           Reference in which BAR1 memory
     *                                             information is returned.
     *
     * @return
     *         - \ref NVML_SUCCESS                 if BAR1 memory is successfully retrieved
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid, \a bar1Memory is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if this query is not supported by the device
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     *
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetBAR1MemoryInfo
    """
    c_bar1_memory = c_nvmlBAR1Memory_t()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetBAR1MemoryInfo")
    ret = fn(handle, byref(c_bar1_memory))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_bar1_memory)

def nvmlDeviceGetComputeMode(handle):
    r"""
    /**
     * Retrieves the current compute mode for the device.
     *
     * For all products.
     *
     * See \ref nvmlComputeMode_t for details on allowed compute modes.
     *
     * @param device                               The identifier of the target device
     * @param mode                                 Reference in which to return the current compute mode
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a mode has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or \a mode is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not support this feature
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     *
     * @see nvmlDeviceSetComputeMode()
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetComputeMode
    """
    c_mode = _nvmlComputeMode_t()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetComputeMode")
    ret = fn(handle, byref(c_mode))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_mode.value)

def nvmlDeviceGetEccMode(handle):
    r"""
    /**
     * Retrieves the current and pending ECC modes for the device.
     *
     * For Fermi &tm; or newer fully supported devices.
     * Only applicable to devices with ECC.
     * Requires \a NVML_INFOROM_ECC version 1.0 or higher.
     *
     * Changing ECC modes requires a reboot. The "pending" ECC mode refers to the target mode following
     * the next reboot.
     *
     * See \ref nvmlEnableState_t for details on allowed modes.
     *
     * @param device                               The identifier of the target device
     * @param current                              Reference in which to return the current ECC mode
     * @param pending                              Reference in which to return the pending ECC mode
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a current and \a pending have been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or either \a current or \a pending is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not support this feature
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     *
     * @see nvmlDeviceSetEccMode()
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetEccMode
    """
    c_currState = _nvmlEnableState_t()
    c_pendingState = _nvmlEnableState_t()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetEccMode")
    ret = fn(handle, byref(c_currState), byref(c_pendingState))
    _nvmlCheckReturn(ret)
    return [c_currState.value, c_pendingState.value]

# added to API
def nvmlDeviceGetCurrentEccMode(handle):
    return nvmlDeviceGetEccMode(handle)[0]

# added to API
def nvmlDeviceGetPendingEccMode(handle):
    return nvmlDeviceGetEccMode(handle)[1]

def nvmlDeviceGetTotalEccErrors(handle, errorType, counterType):
    r"""
    /**
     * Retrieves the total ECC error counts for the device.
     *
     * For Fermi &tm; or newer fully supported devices.
     * Only applicable to devices with ECC.
     * Requires \a NVML_INFOROM_ECC version 1.0 or higher.
     * Requires ECC Mode to be enabled.
     *
     * The total error count is the sum of errors across each of the separate memory systems, i.e. the total set of
     * errors across the entire device.
     *
     * See \ref nvmlMemoryErrorType_t for a description of available error types.\n
     * See \ref nvmlEccCounterType_t for a description of available counter types.
     *
     * @param device                               The identifier of the target device
     * @param errorType                            Flag that specifies the type of the errors.
     * @param counterType                          Flag that specifies the counter-type of the errors.
     * @param eccCounts                            Reference in which to return the specified ECC errors
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a eccCounts has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device, \a errorType or \a counterType is invalid, or \a eccCounts is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not support this feature
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     *
     * @see nvmlDeviceClearEccErrorCounts()
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetTotalEccErrors
    """
    c_count = c_ulonglong()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetTotalEccErrors")
    ret = fn(handle, _nvmlMemoryErrorType_t(errorType),
	         _nvmlEccCounterType_t(counterType), byref(c_count))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_count.value)

# This is deprecated, instead use nvmlDeviceGetMemoryErrorCounter
def nvmlDeviceGetDetailedEccErrors(handle, errorType, counterType):
    r"""
    /**
     * Retrieves the detailed ECC error counts for the device.
     *
     * @deprecated   This API supports only a fixed set of ECC error locations
     *               On different GPU architectures different locations are supported
     *               See \ref nvmlDeviceGetMemoryErrorCounter
     *
     * For Fermi &tm; or newer fully supported devices.
     * Only applicable to devices with ECC.
     * Requires \a NVML_INFOROM_ECC version 2.0 or higher to report aggregate location-based ECC counts.
     * Requires \a NVML_INFOROM_ECC version 1.0 or higher to report all other ECC counts.
     * Requires ECC Mode to be enabled.
     *
     * Detailed errors provide separate ECC counts for specific parts of the memory system.
     *
     * Reports zero for unsupported ECC error counters when a subset of ECC error counters are supported.
     *
     * See \ref nvmlMemoryErrorType_t for a description of available bit types.\n
     * See \ref nvmlEccCounterType_t for a description of available counter types.\n
     * See \ref nvmlEccErrorCounts_t for a description of provided detailed ECC counts.
     *
     * @param device                               The identifier of the target device
     * @param errorType                            Flag that specifies the type of the errors.
     * @param counterType                          Flag that specifies the counter-type of the errors.
     * @param eccCounts                            Reference in which to return the specified ECC errors
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a eccCounts has been populated
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device, \a errorType or \a counterType is invalid, or \a eccCounts is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not support this feature
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     *
     * @see nvmlDeviceClearEccErrorCounts()
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetDetailedEccErrors
    """
    c_counts = c_nvmlEccErrorCounts_t()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetDetailedEccErrors")
    ret = fn(handle, _nvmlMemoryErrorType_t(errorType),
	         _nvmlEccCounterType_t(counterType), byref(c_counts))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_counts)

# Added in 4.304
def nvmlDeviceGetMemoryErrorCounter(handle, errorType, counterType, locationType):
    r"""
    /**
     * Retrieves the requested memory error counter for the device.
     *
     * For Fermi &tm; or newer fully supported devices.
     * Requires \a NVML_INFOROM_ECC version 2.0 or higher to report aggregate location-based memory error counts.
     * Requires \a NVML_INFOROM_ECC version 1.0 or higher to report all other memory error counts.
     *
     * Only applicable to devices with ECC.
     *
     * Requires ECC Mode to be enabled.
     *
     * See \ref nvmlMemoryErrorType_t for a description of available memory error types.\n
     * See \ref nvmlEccCounterType_t for a description of available counter types.\n
     * See \ref nvmlMemoryLocation_t for a description of available counter locations.\n
     *
     * @param device                               The identifier of the target device
     * @param errorType                            Flag that specifies the type of error.
     * @param counterType                          Flag that specifies the counter-type of the errors.
     * @param locationType                         Specifies the location of the counter.
     * @param count                                Reference in which to return the ECC counter
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a count has been populated
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device, \a bitTyp,e \a counterType or \a locationType is
     *                                             invalid, or \a count is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not support ECC error reporting in the specified memory
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetMemoryErrorCounter
    """
    c_count = c_ulonglong()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetMemoryErrorCounter")
    ret = fn(handle,
             _nvmlMemoryErrorType_t(errorType),
             _nvmlEccCounterType_t(counterType),
             _nvmlMemoryLocation_t(locationType),
             byref(c_count))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_count.value)

def nvmlDeviceGetUtilizationRates(handle):
    r"""
    /**
     * Retrieves the current utilization rates for the device's major subsystems.
     *
     * For Fermi &tm; or newer fully supported devices.
     *
     * See \ref nvmlUtilization_t for details on available utilization rates.
     *
     * \note During driver initialization when ECC is enabled one can see high GPU and Memory Utilization readings.
     *       This is caused by ECC Memory Scrubbing mechanism that is performed during driver initialization.
     *
     * @param device                               The identifier of the target device
     * @param utilization                          Reference in which to return the utilization information
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a utilization has been populated
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or \a utilization is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not support this feature
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetUtilizationRates
    """
    c_util = c_nvmlUtilization_t()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetUtilizationRates")
    ret = fn(handle, byref(c_util))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_util)

def nvmlDeviceGetEncoderUtilization(handle):
    r"""
    /**
     * Retrieves the current utilization and sampling size in microseconds for the Encoder
     *
     * For Kepler &tm; or newer fully supported devices.
     *
     * @param device                               The identifier of the target device
     * @param utilization                          Reference to an unsigned int for encoder utilization info
     * @param samplingPeriodUs                     Reference to an unsigned int for the sampling period in US
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a utilization has been populated
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid, \a utilization is NULL, or \a samplingPeriodUs is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not support this feature
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetEncoderUtilization
    """
    c_util = c_uint()
    c_samplingPeriod = c_uint()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetEncoderUtilization")
    ret = fn(handle, byref(c_util), byref(c_samplingPeriod))
    _nvmlCheckReturn(ret)
    return [c_util.value, c_samplingPeriod.value]

def nvmlDeviceGetDecoderUtilization(handle):
    r"""
    /**
     * Retrieves the current utilization and sampling size in microseconds for the Decoder
     *
     * For Kepler &tm; or newer fully supported devices.
     *
     * @param device                               The identifier of the target device
     * @param utilization                          Reference to an unsigned int for decoder utilization info
     * @param samplingPeriodUs                     Reference to an unsigned int for the sampling period in US
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a utilization has been populated
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid, \a utilization is NULL, or \a samplingPeriodUs is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not support this feature
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetDecoderUtilization
    """
    c_util = c_uint()
    c_samplingPeriod = c_uint()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetDecoderUtilization")
    ret = fn(handle, byref(c_util), byref(c_samplingPeriod))
    _nvmlCheckReturn(ret)
    return [c_util.value, c_samplingPeriod.value]

def nvmlDeviceGetPcieReplayCounter(handle):
    r"""
    /**
     * Retrieve the PCIe replay counter.
     *
     * For Kepler &tm; or newer fully supported devices.
     *
     * @param device                               The identifier of the target device
     * @param value                                Reference in which to return the counter's value
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a value has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid, or \a value is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not support this feature
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetPcieReplayCounter
    """
    c_replay = c_uint()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetPcieReplayCounter")
    ret = fn(handle, byref(c_replay))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_replay.value)

def nvmlDeviceGetDriverModel(handle):
    r"""
    /**
     * Retrieves the current and pending driver model for the device.
     *
     * For Fermi &tm; or newer fully supported devices.
     * For windows only.
     *
     * On Windows platforms the device driver can run in either WDDM or WDM (TCC) mode. If a display is attached
     * to the device it must run in WDDM mode. TCC mode is preferred if a display is not attached.
     *
     * See \ref nvmlDriverModel_t for details on available driver models.
     *
     * @param device                               The identifier of the target device
     * @param current                              Reference in which to return the current driver model
     * @param pending                              Reference in which to return the pending driver model
     *
     * @return
     *         - \ref NVML_SUCCESS                 if either \a current and/or \a pending have been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or both \a current and \a pending are NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the platform is not windows
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     *
     * @see nvmlDeviceSetDriverModel()
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetDriverModel
    """
    c_currModel = _nvmlDriverModel_t()
    c_pendingModel = _nvmlDriverModel_t()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetDriverModel")
    ret = fn(handle, byref(c_currModel), byref(c_pendingModel))
    _nvmlCheckReturn(ret)
    return [c_currModel.value, c_pendingModel.value]

# added to API
def nvmlDeviceGetCurrentDriverModel(handle):
    return nvmlDeviceGetDriverModel(handle)[0]

# added to API
def nvmlDeviceGetPendingDriverModel(handle):
    return nvmlDeviceGetDriverModel(handle)[1]

# Added in 2.285
def nvmlDeviceGetVbiosVersion(handle):
    r"""
    /**
     * Get VBIOS version of the device.
     *
     * For all products.
     *
     * The VBIOS version may change from time to time. It will not exceed 32 characters in length
     * (including the NULL terminator).  See \ref nvmlConstants::NVML_DEVICE_VBIOS_VERSION_BUFFER_SIZE.
     *
     * @param device                               The identifier of the target device
     * @param version                              Reference to which to return the VBIOS version
     * @param length                               The maximum allowed length of the string returned in \a version
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a version has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid, or \a version is NULL
     *         - \ref NVML_ERROR_INSUFFICIENT_SIZE if \a length is too small
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetVbiosVersion
    """
    c_version = create_string_buffer(NVML_DEVICE_VBIOS_VERSION_BUFFER_SIZE)
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetVbiosVersion")
    ret = fn(handle, c_version, c_uint(NVML_DEVICE_VBIOS_VERSION_BUFFER_SIZE))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_version.value)

# Added in 2.285
def nvmlDeviceGetComputeRunningProcesses(handle):
    r"""
    /**
     * Get information about processes with a compute context on a device
     *
     * For Fermi &tm; or newer fully supported devices.
     *
     * This function returns information only about compute running processes (e.g. CUDA application which have
     * active context). Any graphics applications (e.g. using OpenGL, DirectX) won't be listed by this function.
     *
     * To query the current number of running compute processes, call this function with *infoCount = 0. The
     * return code will be NVML_ERROR_INSUFFICIENT_SIZE, or NVML_SUCCESS if none are running. For this call
     * \a infos is allowed to be NULL.
     *
     * The usedGpuMemory field returned is all of the memory used by the application.
     *
     * Keep in mind that information returned by this call is dynamic and the number of elements might change in
     * time. Allocate more space for \a infos table in case new compute processes are spawned.
     *
     * @param device                               The identifier of the target device
     * @param infoCount                            Reference in which to provide the \a infos array size, and
     *                                             to return the number of returned elements
     * @param infos                                Reference in which to return the process information
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a infoCount and \a infos have been populated
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INSUFFICIENT_SIZE if \a infoCount indicates that the \a infos array is too small
     *                                             \a infoCount will contain minimal amount of space necessary for
     *                                             the call to complete
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid, either of \a infoCount or \a infos is NULL
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     *
     * @see \ref nvmlSystemGetProcessName
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetComputeRunningProcesses
    """
    # first call to get the size
    c_count = c_uint(0)
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetComputeRunningProcesses")
    ret = fn(handle, byref(c_count), None)

    if (ret == NVML_SUCCESS):
        # special case, no running processes
        return []
    elif (ret == NVML_ERROR_INSUFFICIENT_SIZE):
        # typical case
        # oversize the array incase more processes are created
        c_count.value = c_count.value * 2 + 5
        proc_array = c_nvmlProcessInfo_t * c_count.value
        c_procs = proc_array()

        # make the call again
        ret = fn(handle, byref(c_count), c_procs)
        _nvmlCheckReturn(ret)

        procs = []
        for i in range(c_count.value):
            # use an alternative struct for this object
            obj = nvmlStructToFriendlyObject(c_procs[i])
            if (obj.usedGpuMemory == NVML_VALUE_NOT_AVAILABLE_ulonglong.value):
                # special case for WDDM on Windows, see comment above
                obj.usedGpuMemory = None
            procs.append(obj)

        return procs
    else:
        # error case
        raise NVMLError(ret)

def nvmlDeviceGetGraphicsRunningProcesses(handle):
    r"""
    /**
     * Get information about processes with a graphics context on a device
     *
     * For Kepler &tm; or newer fully supported devices.
     *
     * This function returns information only about graphics based processes
     * (eg. applications using OpenGL, DirectX)
     *
     * To query the current number of running graphics processes, call this function with *infoCount = 0. The
     * return code will be NVML_ERROR_INSUFFICIENT_SIZE, or NVML_SUCCESS if none are running. For this call
     * \a infos is allowed to be NULL.
     *
     * The usedGpuMemory field returned is all of the memory used by the application.
     *
     * Keep in mind that information returned by this call is dynamic and the number of elements might change in
     * time. Allocate more space for \a infos table in case new graphics processes are spawned.
     *
     * @param device                               The identifier of the target device
     * @param infoCount                            Reference in which to provide the \a infos array size, and
     *                                             to return the number of returned elements
     * @param infos                                Reference in which to return the process information
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a infoCount and \a infos have been populated
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INSUFFICIENT_SIZE if \a infoCount indicates that the \a infos array is too small
     *                                             \a infoCount will contain minimal amount of space necessary for
     *                                             the call to complete
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid, either of \a infoCount or \a infos is NULL
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     *
     * @see \ref nvmlSystemGetProcessName
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetGraphicsRunningProcesses
    """
    # first call to get the size
    c_count = c_uint(0)
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetGraphicsRunningProcesses")
    ret = fn(handle, byref(c_count), None)

    if (ret == NVML_SUCCESS):
        # special case, no running processes
        return []
    elif (ret == NVML_ERROR_INSUFFICIENT_SIZE):
        # typical case
        # oversize the array incase more processes are created
        c_count.value = c_count.value * 2 + 5
        proc_array = c_nvmlProcessInfo_t * c_count.value
        c_procs = proc_array()

        # make the call again
        ret = fn(handle, byref(c_count), c_procs)
        _nvmlCheckReturn(ret)

        procs = []
        for i in range(c_count.value):
            # use an alternative struct for this object
            obj = nvmlStructToFriendlyObject(c_procs[i])
            if (obj.usedGpuMemory == NVML_VALUE_NOT_AVAILABLE_ulonglong.value):
                # special case for WDDM on Windows, see comment above
                obj.usedGpuMemory = None
            procs.append(obj)

        return procs
    else:
        # error case
        raise NVMLError(ret)

def nvmlDeviceGetAutoBoostedClocksEnabled(handle):
    r"""
    /**
     * Retrieve the current state of Auto Boosted clocks on a device and store it in \a isEnabled
     *
     * For Kepler &tm; or newer fully supported devices.
     *
     * Auto Boosted clocks are enabled by default on some hardware, allowing the GPU to run at higher clock rates
     * to maximize performance as thermal limits allow.
     *
     * On Pascal and newer hardware, Auto Aoosted clocks are controlled through application clocks.
     * Use \ref nvmlDeviceSetApplicationsClocks and \ref nvmlDeviceResetApplicationsClocks to control Auto Boost
     * behavior.
     *
     * @param device                               The identifier of the target device
     * @param isEnabled                            Where to store the current state of Auto Boosted clocks of the target device
     * @param defaultIsEnabled                     Where to store the default Auto Boosted clocks behavior of the target device that the device will
     *                                                 revert to when no applications are using the GPU
     *
     * @return
     *         - \ref NVML_SUCCESS                 If \a isEnabled has been been set with the Auto Boosted clocks state of \a device
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or \a isEnabled is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not support Auto Boosted clocks
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     *
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetAutoBoostedClocksEnabled
    """
    c_isEnabled = _nvmlEnableState_t()
    c_defaultIsEnabled = _nvmlEnableState_t()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetAutoBoostedClocksEnabled")
    ret = fn(handle, byref(c_isEnabled), byref(c_defaultIsEnabled))
    _nvmlCheckReturn(ret)
    return [c_isEnabled.value, c_defaultIsEnabled.value]
    #Throws NVML_ERROR_NOT_SUPPORTED if hardware doesn't support setting auto boosted clocks

## Set functions
def nvmlUnitSetLedState(unit, color):
    r"""
    /**
     * Set the LED state for the unit. The LED can be either green (0) or amber (1).
     *
     * For S-class products.
     * Requires root/admin permissions.
     *
     * This operation takes effect immediately.
     *
     *
     * <b>Current S-Class products don't provide unique LEDs for each unit. As such, both front
     * and back LEDs will be toggled in unison regardless of which unit is specified with this command.</b>
     *
     * See \ref nvmlLedColor_t for available colors.
     *
     * @param unit                                 The identifier of the target unit
     * @param color                                The target LED color
     *
     * @return
     *         - \ref NVML_SUCCESS                 if the LED color has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a unit or \a color is invalid
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if this is not an S-class product
     *         - \ref NVML_ERROR_NO_PERMISSION     if the user doesn't have permission to perform this operation
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     *
     * @see nvmlUnitGetLedState()
     */
    nvmlReturn_t DECLDIR nvmlUnitSetLedState
    """
    fn = _nvmlGetFunctionPointer("nvmlUnitSetLedState")
    ret = fn(unit, _nvmlLedColor_t(color))
    _nvmlCheckReturn(ret)
    return None

def nvmlDeviceSetPersistenceMode(handle, mode):
    r"""
    /**
     * Set the persistence mode for the device.
     *
     * For all products.
     * For Linux only.
     * Requires root/admin permissions.
     *
     * The persistence mode determines whether the GPU driver software is torn down after the last client
     * exits.
     *
     * This operation takes effect immediately. It is not persistent across reboots. After each reboot the
     * persistence mode is reset to "Disabled".
     *
     * See \ref nvmlEnableState_t for available modes.
     *
     * @param device                               The identifier of the target device
     * @param mode                                 The target persistence mode
     *
     * @return
     *         - \ref NVML_SUCCESS                 if the persistence mode was set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or \a mode is invalid
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not support this feature
     *         - \ref NVML_ERROR_NO_PERMISSION     if the user doesn't have permission to perform this operation
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     *
     * @see nvmlDeviceGetPersistenceMode()
     */
    nvmlReturn_t DECLDIR nvmlDeviceSetPersistenceMode
    """
    fn = _nvmlGetFunctionPointer("nvmlDeviceSetPersistenceMode")
    ret = fn(handle, _nvmlEnableState_t(mode))
    _nvmlCheckReturn(ret)
    return None

def nvmlDeviceSetComputeMode(handle, mode):
    r"""
    /**
     * Set the compute mode for the device.
     *
     * For all products.
     * Requires root/admin permissions.
     *
     * The compute mode determines whether a GPU can be used for compute operations and whether it can
     * be shared across contexts.
     *
     * This operation takes effect immediately. Under Linux it is not persistent across reboots and
     * always resets to "Default". Under windows it is persistent.
     *
     * Under windows compute mode may only be set to DEFAULT when running in WDDM
     *
     * See \ref nvmlComputeMode_t for details on available compute modes.
     *
     * @param device                               The identifier of the target device
     * @param mode                                 The target compute mode
     *
     * @return
     *         - \ref NVML_SUCCESS                 if the compute mode was set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or \a mode is invalid
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not support this feature
     *         - \ref NVML_ERROR_NO_PERMISSION     if the user doesn't have permission to perform this operation
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     *
     * @see nvmlDeviceGetComputeMode()
     */
    nvmlReturn_t DECLDIR nvmlDeviceSetComputeMode
    """
    fn = _nvmlGetFunctionPointer("nvmlDeviceSetComputeMode")
    ret = fn(handle, _nvmlComputeMode_t(mode))
    _nvmlCheckReturn(ret)
    return None

def nvmlDeviceSetEccMode(handle, mode):
    r"""
    /**
     * Set the ECC mode for the device.
     *
     * For Kepler &tm; or newer fully supported devices.
     * Only applicable to devices with ECC.
     * Requires \a NVML_INFOROM_ECC version 1.0 or higher.
     * Requires root/admin permissions.
     *
     * The ECC mode determines whether the GPU enables its ECC support.
     *
     * This operation takes effect after the next reboot.
     *
     * See \ref nvmlEnableState_t for details on available modes.
     *
     * @param device                               The identifier of the target device
     * @param ecc                                  The target ECC mode
     *
     * @return
     *         - \ref NVML_SUCCESS                 if the ECC mode was set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or \a ecc is invalid
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not support this feature
     *         - \ref NVML_ERROR_NO_PERMISSION     if the user doesn't have permission to perform this operation
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     *
     * @see nvmlDeviceGetEccMode()
     */
    nvmlReturn_t DECLDIR nvmlDeviceSetEccMode
    """
    fn = _nvmlGetFunctionPointer("nvmlDeviceSetEccMode")
    ret = fn(handle, _nvmlEnableState_t(mode))
    _nvmlCheckReturn(ret)
    return None

def nvmlDeviceClearEccErrorCounts(handle, counterType):
    r"""
    /**
     * Clear the ECC error and other memory error counts for the device.
     *
     * For Kepler &tm; or newer fully supported devices.
     * Only applicable to devices with ECC.
     * Requires \a NVML_INFOROM_ECC version 2.0 or higher to clear aggregate location-based ECC counts.
     * Requires \a NVML_INFOROM_ECC version 1.0 or higher to clear all other ECC counts.
     * Requires root/admin permissions.
     * Requires ECC Mode to be enabled.
     *
     * Sets all of the specified ECC counters to 0, including both detailed and total counts.
     *
     * This operation takes effect immediately.
     *
     * See \ref nvmlMemoryErrorType_t for details on available counter types.
     *
     * @param device                               The identifier of the target device
     * @param counterType                          Flag that indicates which type of errors should be cleared.
     *
     * @return
     *         - \ref NVML_SUCCESS                 if the error counts were cleared
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or \a counterType is invalid
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not support this feature
     *         - \ref NVML_ERROR_NO_PERMISSION     if the user doesn't have permission to perform this operation
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     *
     * @see
     *      - nvmlDeviceGetDetailedEccErrors()
     *      - nvmlDeviceGetTotalEccErrors()
     */
    nvmlReturn_t DECLDIR nvmlDeviceClearEccErrorCounts
    """
    fn = _nvmlGetFunctionPointer("nvmlDeviceClearEccErrorCounts")
    ret = fn(handle, _nvmlEccCounterType_t(counterType))
    _nvmlCheckReturn(ret)
    return None

def nvmlDeviceSetDriverModel(handle, model):
    r"""
    /**
     * Set the driver model for the device.
     *
     * For Fermi &tm; or newer fully supported devices.
     * For windows only.
     * Requires root/admin permissions.
     *
     * On Windows platforms the device driver can run in either WDDM or WDM (TCC) mode. If a display is attached
     * to the device it must run in WDDM mode.
     *
     * It is possible to force the change to WDM (TCC) while the display is still attached with a force flag (nvmlFlagForce).
     * This should only be done if the host is subsequently powered down and the display is detached from the device
     * before the next reboot.
     *
     * This operation takes effect after the next reboot.
     *
     * Windows driver model may only be set to WDDM when running in DEFAULT compute mode.
     *
     * Change driver model to WDDM is not supported when GPU doesn't support graphics acceleration or
     * will not support it after reboot. See \ref nvmlDeviceSetGpuOperationMode.
     *
     * See \ref nvmlDriverModel_t for details on available driver models.
     * See \ref nvmlFlagDefault and \ref nvmlFlagForce
     *
     * @param device                               The identifier of the target device
     * @param driverModel                          The target driver model
     * @param flags                                Flags that change the default behavior
     *
     * @return
     *         - \ref NVML_SUCCESS                 if the driver model has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or \a driverModel is invalid
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the platform is not windows or the device does not support this feature
     *         - \ref NVML_ERROR_NO_PERMISSION     if the user doesn't have permission to perform this operation
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     *
     * @see nvmlDeviceGetDriverModel()
     */
    nvmlReturn_t DECLDIR nvmlDeviceSetDriverModel
    """
    fn = _nvmlGetFunctionPointer("nvmlDeviceSetDriverModel")
    ret = fn(handle, _nvmlDriverModel_t(model))
    _nvmlCheckReturn(ret)
    return None

def nvmlDeviceSetAutoBoostedClocksEnabled(handle, enabled):
    r"""
    /**
     * Try to set the current state of Auto Boosted clocks on a device.
     *
     * For Kepler &tm; or newer fully supported devices.
     *
     * Auto Boosted clocks are enabled by default on some hardware, allowing the GPU to run at higher clock rates
     * to maximize performance as thermal limits allow. Auto Boosted clocks should be disabled if fixed clock
     * rates are desired.
     *
     * Non-root users may use this API by default but can be restricted by root from using this API by calling
     * \ref nvmlDeviceSetAPIRestriction with apiType=NVML_RESTRICTED_API_SET_AUTO_BOOSTED_CLOCKS.
     * Note: Persistence Mode is required to modify current Auto Boost settings, therefore, it must be enabled.
     *
     * On Pascal and newer hardware, Auto Boosted clocks are controlled through application clocks.
     * Use \ref nvmlDeviceSetApplicationsClocks and \ref nvmlDeviceResetApplicationsClocks to control Auto Boost
     * behavior.
     *
     * @param device                               The identifier of the target device
     * @param enabled                              What state to try to set Auto Boosted clocks of the target device to
     *
     * @return
     *         - \ref NVML_SUCCESS                 If the Auto Boosted clocks were successfully set to the state specified by \a enabled
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not support Auto Boosted clocks
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     *
     */
    nvmlReturn_t DECLDIR nvmlDeviceSetAutoBoostedClocksEnabled
    """
    fn = _nvmlGetFunctionPointer("nvmlDeviceSetAutoBoostedClocksEnabled")
    ret = fn(handle, _nvmlEnableState_t(enabled))
    _nvmlCheckReturn(ret)
    return None
    #Throws NVML_ERROR_NOT_SUPPORTED if hardware doesn't support setting auto boosted clocks

def nvmlDeviceSetDefaultAutoBoostedClocksEnabled(handle, enabled, flags):
    r"""
    /**
     * Try to set the default state of Auto Boosted clocks on a device. This is the default state that Auto Boosted clocks will
     * return to when no compute running processes (e.g. CUDA application which have an active context) are running
     *
     * For Kepler &tm; or newer non-GeForce fully supported devices and Maxwell or newer GeForce devices.
     * Requires root/admin permissions.
     *
     * Auto Boosted clocks are enabled by default on some hardware, allowing the GPU to run at higher clock rates
     * to maximize performance as thermal limits allow. Auto Boosted clocks should be disabled if fixed clock
     * rates are desired.
     *
     * On Pascal and newer hardware, Auto Boosted clocks are controlled through application clocks.
     * Use \ref nvmlDeviceSetApplicationsClocks and \ref nvmlDeviceResetApplicationsClocks to control Auto Boost
     * behavior.
     *
     * @param device                               The identifier of the target device
     * @param enabled                              What state to try to set default Auto Boosted clocks of the target device to
     * @param flags                                Flags that change the default behavior. Currently Unused.
     *
     * @return
     *         - \ref NVML_SUCCESS                 If the Auto Boosted clock's default state was successfully set to the state specified by \a enabled
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_NO_PERMISSION     If the calling user does not have permission to change Auto Boosted clock's default state.
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not support Auto Boosted clocks
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     *
     */
    nvmlReturn_t DECLDIR nvmlDeviceSetDefaultAutoBoostedClocksEnabled
    """
    fn = _nvmlGetFunctionPointer("nvmlDeviceSetDefaultAutoBoostedClocksEnabled")
    ret = fn(handle, _nvmlEnableState_t(enabled), c_uint(flags))
    _nvmlCheckReturn(ret)
    return None
    #Throws NVML_ERROR_NOT_SUPPORTED if hardware doesn't support setting auto boosted clocks

# Added in 4.304
def nvmlDeviceSetApplicationsClocks(handle, maxMemClockMHz, maxGraphicsClockMHz):
    r"""
    /**
     * Set clocks that applications will lock to.
     *
     * Sets the clocks that compute and graphics applications will be running at.
     * e.g. CUDA driver requests these clocks during context creation which means this property
     * defines clocks at which CUDA applications will be running unless some overspec event
     * occurs (e.g. over power, over thermal or external HW brake).
     *
     * Can be used as a setting to request constant performance.
     *
     * On Pascal and newer hardware, this will automatically disable automatic boosting of clocks.
     *
     * On K80 and newer Kepler and Maxwell GPUs, users desiring fixed performance should also call
     * \ref nvmlDeviceSetAutoBoostedClocksEnabled to prevent clocks from automatically boosting
     * above the clock value being set.
     *
     * For Kepler &tm; or newer non-GeForce fully supported devices and Maxwell or newer GeForce devices.
     * Requires root/admin permissions.
     *
     * See \ref nvmlDeviceGetSupportedMemoryClocks and \ref nvmlDeviceGetSupportedGraphicsClocks
     * for details on how to list available clocks combinations.
     *
     * After system reboot or driver reload applications clocks go back to their default value.
     * See \ref nvmlDeviceResetApplicationsClocks.
     *
     * @param device                               The identifier of the target device
     * @param memClockMHz                          Requested memory clock in MHz
     * @param graphicsClockMHz                     Requested graphics clock in MHz
     *
     * @return
     *         - \ref NVML_SUCCESS                 if new settings were successfully set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or \a memClockMHz and \a graphicsClockMHz
     *                                                 is not a valid clock combination
     *         - \ref NVML_ERROR_NO_PERMISSION     if the user doesn't have permission to perform this operation
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device doesn't support this feature
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceSetApplicationsClocks
    """
    fn = _nvmlGetFunctionPointer("nvmlDeviceSetApplicationsClocks")
    ret = fn(handle, c_uint(maxMemClockMHz), c_uint(maxGraphicsClockMHz))
    _nvmlCheckReturn(ret)
    return None

# Added in 4.304
def nvmlDeviceResetApplicationsClocks(handle):
    r"""
    /**
     * Resets the application clock to the default value
     *
     * This is the applications clock that will be used after system reboot or driver reload.
     * Default value is constant, but the current value an be changed using \ref nvmlDeviceSetApplicationsClocks.
     *
     * On Pascal and newer hardware, if clocks were previously locked with \ref nvmlDeviceSetApplicationsClocks,
     * this call will unlock clocks. This returns clocks their default behavior ofautomatically boosting above
     * base clocks as thermal limits allow.
     *
     * @see nvmlDeviceGetApplicationsClock
     * @see nvmlDeviceSetApplicationsClocks
     *
     * For Fermi &tm; or newer non-GeForce fully supported devices and Maxwell or newer GeForce devices.
     *
     * @param device                               The identifier of the target device
     *
     * @return
     *         - \ref NVML_SUCCESS                 if new settings were successfully set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not support this feature
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceResetApplicationsClocks
    """
    fn = _nvmlGetFunctionPointer("nvmlDeviceResetApplicationsClocks")
    ret = fn(handle)
    _nvmlCheckReturn(ret)
    return None

# Added in 4.304
def nvmlDeviceSetPowerManagementLimit(handle, limit):
    r"""
    /**
     * Set new power limit of this device.
     *
     * For Kepler &tm; or newer fully supported devices.
     * Requires root/admin permissions.
     *
     * See \ref nvmlDeviceGetPowerManagementLimitConstraints to check the allowed ranges of values.
     *
     * \note Limit is not persistent across reboots or driver unloads.
     * Enable persistent mode to prevent driver from unloading when no application is using the device.
     *
     * @param device                               The identifier of the target device
     * @param limit                                Power management limit in milliwatts to set
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a limit has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or \a defaultLimit is out of range
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not support this feature
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     *
     * @see nvmlDeviceGetPowerManagementLimitConstraints
     * @see nvmlDeviceGetPowerManagementDefaultLimit
     */
    nvmlReturn_t DECLDIR nvmlDeviceSetPowerManagementLimit
    """
    fn = _nvmlGetFunctionPointer("nvmlDeviceSetPowerManagementLimit")
    ret = fn(handle, c_uint(limit))
    _nvmlCheckReturn(ret)
    return None

# Added in 4.304
def nvmlDeviceSetGpuOperationMode(handle, mode):
    r"""
    /**
     * Sets new GOM. See \a nvmlGpuOperationMode_t for details.
     *
     * For GK110 M-class and X-class Tesla &tm; products from the Kepler family.
     * Modes \ref NVML_GOM_LOW_DP and \ref NVML_GOM_ALL_ON are supported on fully supported GeForce products.
     * Not supported on Quadro &reg; and Tesla &tm; C-class products.
     * Requires root/admin permissions.
     *
     * Changing GOMs requires a reboot.
     * The reboot requirement might be removed in the future.
     *
     * Compute only GOMs don't support graphics acceleration. Under windows switching to these GOMs when
     * pending driver model is WDDM is not supported. See \ref nvmlDeviceSetDriverModel.
     *
     * @param device                               The identifier of the target device
     * @param mode                                 Target GOM
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a mode has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or \a mode incorrect
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not support GOM or specific mode
     *         - \ref NVML_ERROR_NO_PERMISSION     if the user doesn't have permission to perform this operation
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     *
     * @see nvmlGpuOperationMode_t
     * @see nvmlDeviceGetGpuOperationMode
     */
    nvmlReturn_t DECLDIR nvmlDeviceSetGpuOperationMode
    """
    fn = _nvmlGetFunctionPointer("nvmlDeviceSetGpuOperationMode")
    ret = fn(handle, _nvmlGpuOperationMode_t(mode))
    _nvmlCheckReturn(ret)
    return None

# Added in 2.285
def nvmlEventSetCreate():
    r"""
    /**
     * Create an empty set of events.
     * Event set should be freed by \ref nvmlEventSetFree
     *
     * For Fermi &tm; or newer fully supported devices.
     * @param set                                  Reference in which to return the event handle
     *
     * @return
     *         - \ref NVML_SUCCESS                 if the event has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a set is NULL
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     *
     * @see nvmlEventSetFree
     */
    nvmlReturn_t DECLDIR nvmlEventSetCreate
    """
    fn = _nvmlGetFunctionPointer("nvmlEventSetCreate")
    eventSet = c_nvmlEventSet_t()
    ret = fn(byref(eventSet))
    _nvmlCheckReturn(ret)
    return eventSet

# Added in 2.285
def nvmlDeviceRegisterEvents(handle, eventTypes, eventSet):
    r"""
    /**
     * Starts recording of events on a specified devices and add the events to specified \ref nvmlEventSet_t
     *
     * For Fermi &tm; or newer fully supported devices.
     * Ecc events are available only on ECC enabled devices (see \ref nvmlDeviceGetTotalEccErrors)
     * Power capping events are available only on Power Management enabled devices (see \ref nvmlDeviceGetPowerManagementMode)
     *
     * For Linux only.
     *
     * \b IMPORTANT: Operations on \a set are not thread safe
     *
     * This call starts recording of events on specific device.
     * All events that occurred before this call are not recorded.
     * Checking if some event occurred can be done with \ref nvmlEventSetWait
     *
     * If function reports NVML_ERROR_UNKNOWN, event set is in undefined state and should be freed.
     * If function reports NVML_ERROR_NOT_SUPPORTED, event set can still be used. None of the requested eventTypes
     *     are registered in that case.
     *
     * @param device                               The identifier of the target device
     * @param eventTypes                           Bitmask of \ref nvmlEventType to record
     * @param set                                  Set to which add new event types
     *
     * @return
     *         - \ref NVML_SUCCESS                 if the event has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a eventTypes is invalid or \a set is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the platform does not support this feature or some of requested event types
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     *
     * @see nvmlEventType
     * @see nvmlDeviceGetSupportedEventTypes
     * @see nvmlEventSetWait
     * @see nvmlEventSetFree
     */
    nvmlReturn_t DECLDIR nvmlDeviceRegisterEvents
    """
    fn = _nvmlGetFunctionPointer("nvmlDeviceRegisterEvents")
    ret = fn(handle, c_ulonglong(eventTypes), eventSet)
    _nvmlCheckReturn(ret)
    return None

# Added in 2.285
def nvmlDeviceGetSupportedEventTypes(handle):
    r"""
    /**
     * Returns information about events supported on device
     *
     * For Fermi &tm; or newer fully supported devices.
     *
     * Events are not supported on Windows. So this function returns an empty mask in \a eventTypes on Windows.
     *
     * @param device                               The identifier of the target device
     * @param eventTypes                           Reference in which to return bitmask of supported events
     *
     * @return
     *         - \ref NVML_SUCCESS                 if the eventTypes has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a eventType is NULL
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     *
     * @see nvmlEventType
     * @see nvmlDeviceRegisterEvents
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetSupportedEventTypes
    """
    c_eventTypes = c_ulonglong()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetSupportedEventTypes")
    ret = fn(handle, byref(c_eventTypes))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_eventTypes.value)

# Added in 2.285
# raises NVML_ERROR_TIMEOUT exception on timeout
def nvmlEventSetWait(eventSet, timeoutms):
    r"""
    /**
     * Waits on events and delivers events
     *
     * For Fermi &tm; or newer fully supported devices.
     *
     * If some events are ready to be delivered at the time of the call, function returns immediately.
     * If there are no events ready to be delivered, function sleeps till event arrives
     * but not longer than specified timeout. This function in certain conditions can return before
     * specified timeout passes (e.g. when interrupt arrives)
     *
     * In case of xid error, the function returns the most recent xid error type seen by the system. If there are multiple
     * xid errors generated before nvmlEventSetWait is invoked then the last seen xid error type is returned for all
     * xid error events.
     *
     * @param set                                  Reference to set of events to wait on
     * @param data                                 Reference in which to return event data
     * @param timeoutms                            Maximum amount of wait time in milliseconds for registered event
     *
     * @return
     *         - \ref NVML_SUCCESS                 if the data has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a data is NULL
     *         - \ref NVML_ERROR_TIMEOUT           if no event arrived in specified timeout or interrupt arrived
     *         - \ref NVML_ERROR_GPU_IS_LOST       if a GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     *
     * @see nvmlEventType
     * @see nvmlDeviceRegisterEvents
     */
    nvmlReturn_t DECLDIR nvmlEventSetWait
    """
    fn = _nvmlGetFunctionPointer("nvmlEventSetWait")
    data = c_nvmlEventData_t()
    ret = fn(eventSet, byref(data), c_uint(timeoutms))
    _nvmlCheckReturn(ret)
    return bytes_to_str(data)

# Added in 2.285
def nvmlEventSetFree(eventSet):
    r"""
    /**
     * Releases events in the set
     *
     * For Fermi &tm; or newer fully supported devices.
     *
     * @param set                                  Reference to events to be released
     *
     * @return
     *         - \ref NVML_SUCCESS                 if the event has been successfully released
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     *
     * @see nvmlDeviceRegisterEvents
     */
    nvmlReturn_t DECLDIR nvmlEventSetFree
    """
    fn = _nvmlGetFunctionPointer("nvmlEventSetFree")
    ret = fn(eventSet)
    _nvmlCheckReturn(ret)
    return None

# Added in 3.295
def nvmlDeviceOnSameBoard(handle1, handle2):
    r"""
    /**
     * Check if the GPU devices are on the same physical board.
     *
     * For all fully supported products.
     *
     * @param device1                               The first GPU device
     * @param device2                               The second GPU device
     * @param onSameBoard                           Reference in which to return the status.
     *                                              Non-zero indicates that the GPUs are on the same board.
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a onSameBoard has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a dev1 or \a dev2 are invalid or \a onSameBoard is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if this check is not supported by the device
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the either GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceOnSameBoard
    """
    fn = _nvmlGetFunctionPointer("nvmlDeviceOnSameBoard")
    onSameBoard = c_int()
    ret = fn(handle1, handle2, byref(onSameBoard))
    _nvmlCheckReturn(ret)
    return (onSameBoard.value != 0)

# Added in 3.295
def nvmlDeviceGetCurrPcieLinkGeneration(handle):
    r"""
    /**
     * Retrieves the current PCIe link generation
     *
     * For Fermi &tm; or newer fully supported devices.
     *
     * @param device                               The identifier of the target device
     * @param currLinkGen                          Reference in which to return the current PCIe link generation
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a currLinkGen has been populated
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or \a currLinkGen is null
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if PCIe link information is not available
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetCurrPcieLinkGeneration
    """
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetCurrPcieLinkGeneration")
    gen = c_uint()
    ret = fn(handle, byref(gen))
    _nvmlCheckReturn(ret)
    return bytes_to_str(gen.value)

# Added in 3.295
def nvmlDeviceGetMaxPcieLinkGeneration(handle):
    r"""
    /**
     * Retrieves the maximum PCIe link generation possible with this device and system
     *
     * I.E. for a generation 2 PCIe device attached to a generation 1 PCIe bus the max link generation this function will
     * report is generation 1.
     *
     * For Fermi &tm; or newer fully supported devices.
     *
     * @param device                               The identifier of the target device
     * @param maxLinkGen                           Reference in which to return the max PCIe link generation
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a maxLinkGen has been populated
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or \a maxLinkGen is null
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if PCIe link information is not available
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetMaxPcieLinkGeneration
    """
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetMaxPcieLinkGeneration")
    gen = c_uint()
    ret = fn(handle, byref(gen))
    _nvmlCheckReturn(ret)
    return bytes_to_str(gen.value)

# Added in 3.295
def nvmlDeviceGetCurrPcieLinkWidth(handle):
    r"""
    /**
     * Retrieves the current PCIe link width
     *
     * For Fermi &tm; or newer fully supported devices.
     *
     * @param device                               The identifier of the target device
     * @param currLinkWidth                        Reference in which to return the current PCIe link generation
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a currLinkWidth has been populated
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or \a currLinkWidth is null
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if PCIe link information is not available
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetCurrPcieLinkWidth
    """
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetCurrPcieLinkWidth")
    width = c_uint()
    ret = fn(handle, byref(width))
    _nvmlCheckReturn(ret)
    return bytes_to_str(width.value)

# Added in 3.295
def nvmlDeviceGetMaxPcieLinkWidth(handle):
    r"""
    /**
     * Retrieves the maximum PCIe link width possible with this device and system
     *
     * I.E. for a device with a 16x PCIe bus width attached to a 8x PCIe system bus this function will report
     * a max link width of 8.
     *
     * For Fermi &tm; or newer fully supported devices.
     *
     * @param device                               The identifier of the target device
     * @param maxLinkWidth                         Reference in which to return the max PCIe link generation
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a maxLinkWidth has been populated
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or \a maxLinkWidth is null
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if PCIe link information is not available
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetMaxPcieLinkWidth
    """
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetMaxPcieLinkWidth")
    width = c_uint()
    ret = fn(handle, byref(width))
    _nvmlCheckReturn(ret)
    return bytes_to_str(width.value)

# Added in 4.304
def nvmlDeviceGetSupportedClocksThrottleReasons(handle):
    r"""
    /**
     * Retrieves bitmask of supported clocks throttle reasons that can be returned by
     * \ref nvmlDeviceGetCurrentClocksThrottleReasons
     *
     * For all fully supported products.
     *
     * This method is not supported in virtual machines running virtual GPU (vGPU).
     *
     * @param device                               The identifier of the target device
     * @param supportedClocksThrottleReasons       Reference in which to return bitmask of supported
     *                                              clocks throttle reasons
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a supportedClocksThrottleReasons has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or \a supportedClocksThrottleReasons is NULL
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     *
     * @see nvmlClocksThrottleReasons
     * @see nvmlDeviceGetCurrentClocksThrottleReasons
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetSupportedClocksThrottleReasons
    """
    c_reasons= c_ulonglong()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetSupportedClocksThrottleReasons")
    ret = fn(handle, byref(c_reasons))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_reasons.value)

# Added in 4.304
def nvmlDeviceGetCurrentClocksThrottleReasons(handle):
    r"""
    /**
     * Retrieves current clocks throttling reasons.
     *
     * For all fully supported products.
     *
     * \note More than one bit can be enabled at the same time. Multiple reasons can be affecting clocks at once.
     *
     * @param device                                The identifier of the target device
     * @param clocksThrottleReasons                 Reference in which to return bitmask of active clocks throttle
     *                                                  reasons
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a clocksThrottleReasons has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or \a clocksThrottleReasons is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not support this feature
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     *
     * @see nvmlClocksThrottleReasons
     * @see nvmlDeviceGetSupportedClocksThrottleReasons
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetCurrentClocksThrottleReasons
    """
    c_reasons= c_ulonglong()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetCurrentClocksThrottleReasons")
    ret = fn(handle, byref(c_reasons))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_reasons.value)

# Added in 5.319
def nvmlDeviceGetIndex(handle):
    r"""
    /**
     * Retrieves the NVML index of this device.
     *
     * For all products.
     *
     * Valid indices are derived from the \a accessibleDevices count returned by
     *   \ref nvmlDeviceGetCount(). For example, if \a accessibleDevices is 2 the valid indices
     *   are 0 and 1, corresponding to GPU 0 and GPU 1.
     *
     * The order in which NVML enumerates devices has no guarantees of consistency between reboots. For that reason it
     *   is recommended that devices be looked up by their PCI ids or GPU UUID. See
     *   \ref nvmlDeviceGetHandleByPciBusId() and \ref nvmlDeviceGetHandleByUUID().
     *
     * Note: The NVML index may not correlate with other APIs, such as the CUDA device index.
     *
     * @param device                               The identifier of the target device
     * @param index                                Reference in which to return the NVML index of the device
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a index has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid, or \a index is NULL
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     *
     * @see nvmlDeviceGetHandleByIndex()
     * @see nvmlDeviceGetCount()
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetIndex
    """
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetIndex")
    c_index = c_uint()
    ret = fn(handle, byref(c_index))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_index.value)


# Added in 5.319
def nvmlDeviceGetAccountingMode(handle):
    r"""
    /**
     * Queries the state of per process accounting mode.
     *
     * For Kepler &tm; or newer fully supported devices.
     *
     * See \ref nvmlDeviceGetAccountingStats for more details.
     * See \ref nvmlDeviceSetAccountingMode
     *
     * @param device                               The identifier of the target device
     * @param mode                                 Reference in which to return the current accounting mode
     *
     * @return
     *         - \ref NVML_SUCCESS                 if the mode has been successfully retrieved
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or \a mode are NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device doesn't support this feature
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetAccountingMode
    """
    c_mode = _nvmlEnableState_t()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetAccountingMode")
    ret = fn(handle, byref(c_mode))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_mode.value)


def nvmlDeviceSetAccountingMode(handle, mode):
    r"""
    /**
     * Enables or disables per process accounting.
     *
     * For Kepler &tm; or newer fully supported devices.
     * Requires root/admin permissions.
     *
     * @note This setting is not persistent and will default to disabled after driver unloads.
     *       Enable persistence mode to be sure the setting doesn't switch off to disabled.
     *
     * @note Enabling accounting mode has no negative impact on the GPU performance.
     *
     * @note Disabling accounting clears all accounting pids information.
     *
     * See \ref nvmlDeviceGetAccountingMode
     * See \ref nvmlDeviceGetAccountingStats
     * See \ref nvmlDeviceClearAccountingPids
     *
     * @param device                               The identifier of the target device
     * @param mode                                 The target accounting mode
     *
     * @return
     *         - \ref NVML_SUCCESS                 if the new mode has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device or \a mode are invalid
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device doesn't support this feature
     *         - \ref NVML_ERROR_NO_PERMISSION     if the user doesn't have permission to perform this operation
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceSetAccountingMode
    """
    fn = _nvmlGetFunctionPointer("nvmlDeviceSetAccountingMode")
    ret = fn(handle, _nvmlEnableState_t(mode))
    _nvmlCheckReturn(ret)
    return None


def nvmlDeviceClearAccountingPids(handle):
    r"""
    /**
     * Clears accounting information about all processes that have already terminated.
     *
     * For Kepler &tm; or newer fully supported devices.
     * Requires root/admin permissions.
     *
     * See \ref nvmlDeviceGetAccountingMode
     * See \ref nvmlDeviceGetAccountingStats
     * See \ref nvmlDeviceSetAccountingMode
     *
     * @param device                               The identifier of the target device
     *
     * @return
     *         - \ref NVML_SUCCESS                 if accounting information has been cleared
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device are invalid
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device doesn't support this feature
     *         - \ref NVML_ERROR_NO_PERMISSION     if the user doesn't have permission to perform this operation
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceClearAccountingPids
    """
    fn = _nvmlGetFunctionPointer("nvmlDeviceClearAccountingPids")
    ret = fn(handle)
    _nvmlCheckReturn(ret)
    return None


def nvmlDeviceGetAccountingStats(handle, pid):
    r"""
    /**
     * Queries process's accounting stats.
     *
     * For Kepler &tm; or newer fully supported devices.
     *
     * Accounting stats capture GPU utilization and other statistics across the lifetime of a process.
     * Accounting stats can be queried during life time of the process and after its termination.
     * The time field in \ref nvmlAccountingStats_t is reported as 0 during the lifetime of the process and
     * updated to actual running time after its termination.
     * Accounting stats are kept in a circular buffer, newly created processes overwrite information about old
     * processes.
     *
     * See \ref nvmlAccountingStats_t for description of each returned metric.
     * List of processes that can be queried can be retrieved from \ref nvmlDeviceGetAccountingPids.
     *
     * @note Accounting Mode needs to be on. See \ref nvmlDeviceGetAccountingMode.
     * @note Only compute and graphics applications stats can be queried. Monitoring applications stats can't be
     *         queried since they don't contribute to GPU utilization.
     * @note In case of pid collision stats of only the latest process (that terminated last) will be reported
     *
     * @warning On Kepler devices per process statistics are accurate only if there's one process running on a GPU.
     *
     * @param device                               The identifier of the target device
     * @param pid                                  Process Id of the target process to query stats for
     * @param stats                                Reference in which to return the process's accounting stats
     *
     * @return
     *         - \ref NVML_SUCCESS                 if stats have been successfully retrieved
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or \a stats are NULL
     *         - \ref NVML_ERROR_NOT_FOUND         if process stats were not found
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device doesn't support this feature or accounting mode is disabled
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     *
     * @see nvmlDeviceGetAccountingBufferSize
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetAccountingStats
    """
    stats = c_nvmlAccountingStats_t()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetAccountingStats")
    ret = fn(handle, c_uint(pid), byref(stats))
    _nvmlCheckReturn(ret)
    if (stats.maxMemoryUsage == NVML_VALUE_NOT_AVAILABLE_ulonglong.value):
        # special case for WDDM on Windows, see comment above
        stats.maxMemoryUsage = None
    return bytes_to_str(stats)


def nvmlDeviceGetAccountingPids(handle):
    r"""
    /**
     * Queries list of processes that can be queried for accounting stats. The list of processes returned
     * can be in running or terminated state.
     *
     * For Kepler &tm; or newer fully supported devices.
     *
     * To just query the number of processes ready to be queried, call this function with *count = 0 and
     * pids=NULL. The return code will be NVML_ERROR_INSUFFICIENT_SIZE, or NVML_SUCCESS if list is empty.
     *
     * For more details see \ref nvmlDeviceGetAccountingStats.
     *
     * @note In case of PID collision some processes might not be accessible before the circular buffer is full.
     *
     * @param device                               The identifier of the target device
     * @param count                                Reference in which to provide the \a pids array size, and
     *                                               to return the number of elements ready to be queried
     * @param pids                                 Reference in which to return list of process ids
     *
     * @return
     *         - \ref NVML_SUCCESS                 if pids were successfully retrieved
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or \a count is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device doesn't support this feature or accounting mode is disabled
     *         - \ref NVML_ERROR_INSUFFICIENT_SIZE if \a count is too small (\a count is set to
     *                                                 expected value)
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     *
     * @see nvmlDeviceGetAccountingBufferSize
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetAccountingPids
    """
    count = c_uint(nvmlDeviceGetAccountingBufferSize(handle))
    pids = (c_uint * count.value)()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetAccountingPids")
    ret = fn(handle, byref(count), pids)
    _nvmlCheckReturn(ret)
    return list(map(int, pids[0:count.value]))


def nvmlDeviceGetAccountingBufferSize(handle):
    r"""
    /**
     * Returns the number of processes that the circular buffer with accounting pids can hold.
     *
     * For Kepler &tm; or newer fully supported devices.
     *
     * This is the maximum number of processes that accounting information will be stored for before information
     * about oldest processes will get overwritten by information about new processes.
     *
     * @param device                               The identifier of the target device
     * @param bufferSize                           Reference in which to provide the size (in number of elements)
     *                                               of the circular buffer for accounting stats.
     *
     * @return
     *         - \ref NVML_SUCCESS                 if buffer size was successfully retrieved
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or \a bufferSize is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device doesn't support this feature or accounting mode is disabled
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     *
     * @see nvmlDeviceGetAccountingStats
     * @see nvmlDeviceGetAccountingPids
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetAccountingBufferSize
    """
    bufferSize = c_uint()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetAccountingBufferSize")
    ret = fn(handle, byref(bufferSize))
    _nvmlCheckReturn(ret)
    return int(bufferSize.value)


def nvmlDeviceGetRetiredPages(device, sourceFilter):
    r"""
    /**
     * Returns the list of retired pages by source, including pages that are pending retirement
     * The address information provided from this API is the hardware address of the page that was retired.  Note
     * that this does not match the virtual address used in CUDA, but will match the address information in XID 63
     *
     * For Kepler &tm; or newer fully supported devices.
     *
     * @param device                            The identifier of the target device
     * @param cause                             Filter page addresses by cause of retirement
     * @param pageCount                         Reference in which to provide the \a addresses buffer size, and
     *                                          to return the number of retired pages that match \a cause
     *                                          Set to 0 to query the size without allocating an \a addresses buffer
     * @param addresses                         Buffer to write the page addresses into
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a pageCount was populated and \a addresses was filled
     *         - \ref NVML_ERROR_INSUFFICIENT_SIZE if \a pageCount indicates the buffer is not large enough to store all the
     *                                             matching page addresses.  \a pageCount is set to the needed size.
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid, \a pageCount is NULL, \a cause is invalid, or
     *                                             \a addresses is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device doesn't support this feature
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetRetiredPages
    """
    c_source = _nvmlPageRetirementCause_t(sourceFilter)
    c_count = c_uint(0)
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetRetiredPages")

    # First call will get the size
    ret = fn(device, c_source, byref(c_count), None)

    # this should only fail with insufficient size
    if ((ret != NVML_SUCCESS) and
        (ret != NVML_ERROR_INSUFFICIENT_SIZE)):
        raise NVMLError(ret)

    # call again with a buffer
    # oversize the array for the rare cases where additional pages
    # are retired between NVML calls
    c_count.value = c_count.value * 2 + 5
    page_array = c_ulonglong * c_count.value
    c_pages = page_array()
    ret = fn(device, c_source, byref(c_count), c_pages)
    _nvmlCheckReturn(ret)
    return list(map(int, c_pages[0:c_count.value]))


def nvmlDeviceGetRetiredPagesPendingStatus(device):
    r"""
    /**
     * Check if any pages are pending retirement and need a reboot to fully retire.
     *
     * For Kepler &tm; or newer fully supported devices.
     *
     * @param device                            The identifier of the target device
     * @param isPending                         Reference in which to return the pending status
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a isPending was populated
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or \a isPending is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device doesn't support this feature
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetRetiredPagesPendingStatus
    """
    c_pending = _nvmlEnableState_t()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetRetiredPagesPendingStatus")
    ret = fn(device, byref(c_pending))
    _nvmlCheckReturn(ret)
    return int(c_pending.value)


def nvmlDeviceGetAPIRestriction(device, apiType):
    r"""
    /**
     * Retrieves the root/admin permissions on the target API. See \a nvmlRestrictedAPI_t for the list of supported APIs.
     * If an API is restricted only root users can call that API. See \a nvmlDeviceSetAPIRestriction to change current permissions.
     *
     * For all fully supported products.
     *
     * @param device                               The identifier of the target device
     * @param apiType                              Target API type for this operation
     * @param isRestricted                         Reference in which to return the current restriction
     *                                             NVML_FEATURE_ENABLED indicates that the API is root-only
     *                                             NVML_FEATURE_DISABLED indicates that the API is accessible to all users
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a isRestricted has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid, \a apiType incorrect or \a isRestricted is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if this query is not supported by the device or the device does not support
     *                                                 the feature that is being queried (E.G. Enabling/disabling Auto Boosted clocks is
     *                                                 not supported by the device)
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     *
     * @see nvmlRestrictedAPI_t
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetAPIRestriction
    """
    c_permission = _nvmlEnableState_t()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetAPIRestriction")
    ret = fn(device, _nvmlRestrictedAPI_t(apiType), byref(c_permission))
    _nvmlCheckReturn(ret)
    return int(c_permission.value)


def nvmlDeviceSetAPIRestriction(handle, apiType, isRestricted):
    r"""
    /**
     * Changes the root/admin restructions on certain APIs. See \a nvmlRestrictedAPI_t for the list of supported APIs.
     * This method can be used by a root/admin user to give non-root/admin access to certain otherwise-restricted APIs.
     * The new setting lasts for the lifetime of the NVIDIA driver; it is not persistent. See \a nvmlDeviceGetAPIRestriction
     * to query the current restriction settings.
     *
     * For Kepler &tm; or newer fully supported devices.
     * Requires root/admin permissions.
     *
     * @param device                               The identifier of the target device
     * @param apiType                              Target API type for this operation
     * @param isRestricted                         The target restriction
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a isRestricted has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid or \a apiType incorrect
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not support changing API restrictions or the device does not support
     *                                                 the feature that api restrictions are being set for (E.G. Enabling/disabling auto
     *                                                 boosted clocks is not supported by the device)
     *         - \ref NVML_ERROR_NO_PERMISSION     if the user doesn't have permission to perform this operation
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     *
     * @see nvmlRestrictedAPI_t
     */
    nvmlReturn_t DECLDIR nvmlDeviceSetAPIRestriction
    """
    fn = _nvmlGetFunctionPointer("nvmlDeviceSetAPIRestriction")
    ret = fn(handle, _nvmlRestrictedAPI_t(apiType), _nvmlEnableState_t(isRestricted))
    _nvmlCheckReturn(ret)
    return None


def nvmlDeviceGetBridgeChipInfo(handle):
    r"""
    /**
     * Get Bridge Chip Information for all the bridge chips on the board.
     *
     * For all fully supported products.
     * Only applicable to multi-GPU products.
     *
     * @param device                                The identifier of the target device
     * @param bridgeHierarchy                       Reference to the returned bridge chip Hierarchy
     *
     * @return
     *         - \ref NVML_SUCCESS                 if bridge chip exists
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid, or \a bridgeInfo is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if bridge chip not supported on the device
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     *
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetBridgeChipInfo
    """
    bridgeHierarchy = c_nvmlBridgeChipHierarchy_t()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetBridgeChipInfo")
    ret = fn(handle, byref(bridgeHierarchy))
    _nvmlCheckReturn(ret)
    return bytes_to_str(bridgeHierarchy)


def nvmlDeviceGetSamples(device, sampling_type, timeStamp):
    r"""
    /**
     * Gets recent samples for the GPU.
     *
     * For Kepler &tm; or newer fully supported devices.
     *
     * Based on type, this method can be used to fetch the power, utilization or clock samples maintained in the buffer by
     * the driver.
     *
     * Power, Utilization and Clock samples are returned as type "unsigned int" for the union nvmlValue_t.
     *
     * To get the size of samples that user needs to allocate, the method is invoked with samples set to NULL.
     * The returned samplesCount will provide the number of samples that can be queried. The user needs to
     * allocate the buffer with size as samplesCount * sizeof(nvmlSample_t).
     *
     * lastSeenTimeStamp represents CPU timestamp in microseconds. Set it to 0 to fetch all the samples maintained by the
     * underlying buffer. Set lastSeenTimeStamp to one of the timeStamps retrieved from the date of the previous query
     * to get more recent samples.
     *
     * This method fetches the number of entries which can be accommodated in the provided samples array, and the
     * reference samplesCount is updated to indicate how many samples were actually retrieved. The advantage of using this
     * method for samples in contrast to polling via existing methods is to get get higher frequency data at lower polling cost.
     *
     * @param device                        The identifier for the target device
     * @param type                          Type of sampling event
     * @param lastSeenTimeStamp             Return only samples with timestamp greater than lastSeenTimeStamp.
     * @param sampleValType                 Output parameter to represent the type of sample value as described in nvmlSampleVal_t
     * @param sampleCount                   Reference to provide the number of elements which can be queried in samples array
     * @param samples                       Reference in which samples are returned

     * @return
     *         - \ref NVML_SUCCESS                 if samples are successfully retrieved
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid, \a samplesCount is NULL or
     *                                             reference to \a sampleCount is 0 for non null \a samples
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if this query is not supported by the device
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_NOT_FOUND         if sample entries are not found
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetSamples
    """
    c_sampling_type = _nvmlSamplingType_t(sampling_type)
    c_time_stamp = c_ulonglong(timeStamp)
    c_sample_count = c_uint(0)
    c_sample_value_type = _nvmlValueType_t()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetSamples")

    ## First Call gets the size
    ret = fn(device, c_sampling_type, c_time_stamp, byref(c_sample_value_type), byref(c_sample_count), None)

    # Stop if this fails
    if (ret != NVML_SUCCESS):
        raise NVMLError(ret)

    sampleArray = c_sample_count.value * c_nvmlSample_t
    c_samples = sampleArray()
    ret = fn(device, c_sampling_type, c_time_stamp,  byref(c_sample_value_type), byref(c_sample_count), c_samples)
    _nvmlCheckReturn(ret)
    return (c_sample_value_type.value, c_samples[0:c_sample_count.value])


def nvmlDeviceGetViolationStatus(device, perfPolicyType):
    r"""
    /**
     * Gets the duration of time during which the device was throttled (lower than requested clocks) due to power
     * or thermal constraints.
     *
     * The method is important to users who are tying to understand if their GPUs throttle at any point during their applications. The
     * difference in violation times at two different reference times gives the indication of GPU throttling event.
     *
     * Violation for thermal capping is not supported at this time.
     *
     * For Kepler &tm; or newer fully supported devices.
     *
     * @param device                               The identifier of the target device
     * @param perfPolicyType                       Represents Performance policy which can trigger GPU throttling
     * @param violTime                             Reference to which violation time related information is returned
     *
     *
     * @return
     *         - \ref NVML_SUCCESS                 if violation time is successfully retrieved
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device is invalid, \a perfPolicyType is invalid, or \a violTime is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if this query is not supported by the device
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetViolationStatus
    """
    c_perfPolicy_type = _nvmlPerfPolicyType_t(perfPolicyType)
    c_violTime = c_nvmlViolationTime_t()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetViolationStatus")

    ## Invoke the method to get violation time
    ret = fn(device, c_perfPolicy_type, byref(c_violTime))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_violTime)


def nvmlDeviceGetPcieThroughput(device, counter):
    r"""
    /**
     * Retrieve PCIe utilization information.
     * This function is querying a byte counter over a 20ms interval and thus is the
     *   PCIe throughput over that interval.
     *
     * For Maxwell &tm; or newer fully supported devices.
     *
     * This method is not supported in virtual machines running virtual GPU (vGPU).
     *
     * @param device                               The identifier of the target device
     * @param counter                              The specific counter that should be queried \ref nvmlPcieUtilCounter_t
     * @param value                                Reference in which to return throughput in KB/s
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a value has been set
     *         - \ref NVML_ERROR_UNINITIALIZED     if the library has not been successfully initialized
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device or \a counter is invalid, or \a value is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device does not support this feature
     *         - \ref NVML_ERROR_GPU_IS_LOST       if the target GPU has fallen off the bus or is otherwise inaccessible
     *         - \ref NVML_ERROR_UNKNOWN           on any unexpected error
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetPcieThroughput
    """
    c_util = c_uint()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetPcieThroughput")
    ret = fn(device, _nvmlPcieUtilCounter_t(counter), byref(c_util))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_util.value)


def nvmlSystemGetTopologyGpuSet(cpuNumber):
    r"""
    /**
     * Retrieve the set of GPUs that have a CPU affinity with the given CPU number
     * For all products.
     * Supported on Linux only.
     *
     * @param cpuNumber                            The CPU number
     * @param count                                When zero, is set to the number of matching GPUs such that \a deviceArray
     *                                             can be malloc'd.  When non-zero, \a deviceArray will be filled with \a count
     *                                             number of device handles.
     * @param deviceArray                          An array of device handles for GPUs found with affinity to \a cpuNumber
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a deviceArray or \a count (if initially zero) has been set
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a cpuNumber, or \a count is invalid, or \a deviceArray is NULL with a non-zero \a count
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device or OS does not support this feature
     *         - \ref NVML_ERROR_UNKNOWN           an error has occurred in underlying topology discovery
     */
    nvmlReturn_t DECLDIR nvmlSystemGetTopologyGpuSet
    """
    c_count = c_uint(0)
    fn = _nvmlGetFunctionPointer("nvmlSystemGetTopologyGpuSet")

    # First call will get the size
    ret = fn(cpuNumber, byref(c_count), None)

    if ret != NVML_SUCCESS:
        raise NVMLError(ret)
    print(c_count.value)
    # call again with a buffer
    device_array = c_nvmlDevice_t * c_count.value
    c_devices = device_array()
    ret = fn(cpuNumber, byref(c_count), c_devices)
    _nvmlCheckReturn(ret)
    return list(c_devices[0:c_count.value])


def nvmlDeviceGetTopologyNearestGpus(device, level):
    r"""
    /**
     * Retrieve the set of GPUs that are nearest to a given device at a specific interconnectivity level
     * For all products.
     * Supported on Linux only.
     *
     * @param device                               The identifier of the first device
     * @param level                                The \ref nvmlGpuTopologyLevel_t level to search for other GPUs
     * @param count                                When zero, is set to the number of matching GPUs such that \a deviceArray
     *                                             can be malloc'd.  When non-zero, \a deviceArray will be filled with \a count
     *                                             number of device handles.
     * @param deviceArray                          An array of device handles for GPUs found at \a level
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a deviceArray or \a count (if initially zero) has been set
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device, \a level, or \a count is invalid, or \a deviceArray is NULL with a non-zero \a count
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device or OS does not support this feature
     *         - \ref NVML_ERROR_UNKNOWN           an error has occurred in underlying topology discovery
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetTopologyNearestGpus
    """
    c_count = c_uint(0)
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetTopologyNearestGpus")

    # First call will get the size
    ret = fn(device, level, byref(c_count), None)

    if ret != NVML_SUCCESS:
        raise NVMLError(ret)

    # call again with a buffer
    device_array = c_nvmlDevice_t * c_count.value
    c_devices = device_array()
    ret = fn(device, level, byref(c_count), c_devices)
    _nvmlCheckReturn(ret)
    return list(c_devices[0:c_count.value])


def nvmlDeviceGetTopologyCommonAncestor(device1, device2):
    r"""
    /**
     * Retrieve the common ancestor for two devices
     * For all products.
     * Supported on Linux only.
     *
     * @param device1                              The identifier of the first device
     * @param device2                              The identifier of the second device
     * @param pathInfo                             A \ref nvmlGpuTopologyLevel_t that gives the path type
     *
     * @return
     *         - \ref NVML_SUCCESS                 if \a pathInfo has been set
     *         - \ref NVML_ERROR_INVALID_ARGUMENT  if \a device1, or \a device2 is invalid, or \a pathInfo is NULL
     *         - \ref NVML_ERROR_NOT_SUPPORTED     if the device or OS does not support this feature
     *         - \ref NVML_ERROR_UNKNOWN           an error has occurred in underlying topology discovery
     */
    nvmlReturn_t DECLDIR nvmlDeviceGetTopologyCommonAncestor
    """
    c_level = _nvmlGpuTopologyLevel_t()
    fn = _nvmlGetFunctionPointer("nvmlDeviceGetTopologyCommonAncestor")
    ret = fn(device1, device2, byref(c_level))
    _nvmlCheckReturn(ret)
    return bytes_to_str(c_level.value)

import ctypes
from ctypes import c_uint8, c_uint16, c_uint32, Structure
from .Api import BaseCommand
from .Commands import Commands
from enum import IntEnum

class ApiHalDeviceIdType(ctypes.c_uint8):
    AHD_NONE = 0
    AHD_UART1 = 1
    AHD_UART2 = 2
    AHD_SPI1 = 3
    AHD_SPI2 = 4
    AHD_TIM0 = 5
    AHD_MAX = 6


class ApiHalDeviceControlType(ctypes.c_uint8):
    AHC_NULL = 0
    AHC_DISABLE = 1
    AHC_ENABLE = 2
    AHC_MAX = 3


class ApiHalLedCmdIdType(ctypes.c_uint8):
    ALI_LED_OFF = 0x00
    ALI_LED_ON = 0x01
    ALI_REPEAT_SEQUENCE = 0x02
    ALI_INVALID = 0xFF


class ApiHalAreaType(ctypes.c_uint8):
    AHA_MEMORY = 0x00
    AHA_REGISTER = 0x01
    AHA_NVS = 0x02
    AHA_DSP = 0x03
    AHA_FPGA = 0x04
    AHA_SEQUENCER = 0x05


class ApiHalGpioPortPinModeType(ctypes.c_uint8):
    GPIO_PORT_PIN_MODE_INPUT = 0x00
    GPIO_PORT_PIN_MODE_INPUT_PULL_UP = 0x01
    GPIO_PORT_PIN_MODE_INPUT_PULL_DOWN = 0x02
    GPIO_PORT_PIN_MODE_OUTPUT = 0x03


class ApiHalGpioPortPinType(ctypes.c_uint8):
    GPIO_PORT_INVALID = 0xFF
    # Additional values can be added as needed


class ApiHalGpioPortType(ctypes.c_uint8):
    GPIO_PORT_P0 = 0x00
    GPIO_PORT_P1 = 0x01
    GPIO_PORT_P2 = 0x02
    GPIO_PORT_P3 = 0x03


class ApiHalGpioPinType(ctypes.c_uint8):
    GPIO_PIN_0 = 0x01
    GPIO_PIN_1 = 0x02
    GPIO_PIN_2 = 0x04
    GPIO_PIN_3 = 0x08
    GPIO_PIN_4 = 0x10
    GPIO_PIN_5 = 0x20
    GPIO_PIN_6 = 0x40
    GPIO_PIN_7 = 0x80


class ApiHalAdcIdType(ctypes.c_uint8):
    ADC_0 = 0x00
    ADC_1 = 0x01
    ADC_2 = 0x02
    CALLER_ID_OUTPUT_AS_INPUT = 0x03
    CODEC_HEADSET_DETECTION = 0x04
    RINGING_OPAMP = 0x05
    VBAT = 0x05
    TEMPERATURE_SENSOR = 0x06
    PARALLEL_SET_DETECTION_OPAMP = 0x07
    MAX_ADC_ENTRIES = 0x08


# Structures


class ApiHalLedCmdType(Structure):
    _pack_ = 1
    _fields_ = [
        ("Command", c_uint8),
        ("Duration", c_uint16),
    ]

    def __init__(self, command: ApiHalLedCmdIdType, duration: int):
        self.Command = command
        self.Duration = duration


class ApiHalEmptySignalType(BaseCommand):

    def __init__(self):
        self.Primitive = Commands.API_HAL_GPIO_FN_REGISTER_REQ


class ApiHalDeviceControlReqType(BaseCommand):
    _fields_ = [
        ("DeviceId", ApiHalDeviceIdType),
        ("Control", ApiHalDeviceControlType),
    ]

    def __init__(self, device_id: ApiHalDeviceIdType, control: ApiHalDeviceControlType):
        self.Primitive = Commands.API_HAL_DEVICE_CONTROL_REQ
        self.DeviceId = device_id
        self.Control = control


class ApiHalDeviceControlCfmType(BaseCommand):
    _fields_ = [
        ("Status", c_uint16),
        ("DeviceId", ApiHalDeviceIdType),
        ("Control", ApiHalDeviceControlType),
    ]

    def __init__(
        self,
        status: int,
        device_id: ApiHalDeviceIdType,
        control: ApiHalDeviceControlType,
    ):
        self.Primitive = Commands.API_HAL_DEVICE_CONTROL_CFM
        self.Statis = status
        self.DeviceId = device_id
        self.Control = control


class ApiHalLedReqType(BaseCommand):
    _pack_ = 1
    _fields_ = [
        ("LedNr", c_uint8),
        ("CmdCount", c_uint8),
        ("Commands", ApiHalLedCmdType * 1),
    ]

    def __init__(self, led: int, commands: list[ApiHalLedCmdType]):
        self.Primitive = Commands.API_HAL_LED_REQ
        self.LedNr = led
        self.CmdCount = len(commands)
        self.set_array(self.Commands, (ApiHalLedCmdType * len(commands))(*commands))


class ApiHalLedCfmType(BaseCommand):
    _fields_ = [
        ("Status", c_uint16),
    ]

    def __init__(self, status: int):
        self.Primitive = Commands.API_HAL_LED_CFM
        self.Status = status


class HalAreaType(IntEnum):
    AHA_MEMORY = 0x00  # Memory mapped area e.g. RAM, flash.
    AHA_REGISTER = 0x01  # Registers. Length must be 1/2/4 bytes for
    #                      8/16/32-bits access.
    AHA_NVS = 0x02  # Non-Volatile Storage (EEPROM).
    AHA_DSP = 0x03  # DSP.
    AHA_FPGA = 0x04  # FPGA.
    AHA_SEQUENCER = 0x05  # Sequencer (DIP).


class ApiHalReadReqType(BaseCommand):
    _fields_ = [
        ("Area", ApiHalAreaType),
        ("Address", c_uint32),
        ("Length", c_uint16),
    ]

    def __init__(self, area: ApiHalAreaType, address: int, length: int):
        self.Primitive = Commands.API_HAL_READ_REQ
        self.Area = area
        self.Address = address
        self.Length = length


def ApiHalReadCfmType(status: int, area: ApiHalAreaType, address: int, data: bytes):
    class ApiHalReadCfmTypeClass(BaseCommand):
        _fields_ = [
            ("Status", c_uint16),
            ("Area", ApiHalAreaType),
            ("Address", c_uint32),
            ("Length", c_uint16),
            ("Data", c_uint8 * len(data)),
        ]

        def __init__(
            self, status: int, area: ApiHalAreaType, address: int, data: bytes
        ):
            self.Primitive = Commands.API_HAL_READ_CFM
            self.Status = status
            self.Area = area
            self.Address = address
            self.Length = len(data)
            self.Data = data

    return ApiHalReadCfmTypeClass(status, area, address, data)


class ApiHalWriteReq(BaseCommand):
    _fields_ = [
        ("Area", ApiHalAreaType),
        ("Address", c_uint32),
        ("Length", c_uint16),
        ("Data", c_uint8 * 1),
    ]

    def __init__(self, area: ApiHalAreaType, address: int, data: bytes):
        self.Primitive = Commands.API_HAL_WRITE_REQ
        self.Area = area
        self.Address = address
        self.Length = len(data)
        self.set_array(self.Data, (c_uint8 * 1)(*data))


class ApiHalWriteCfmType(BaseCommand):
    _fields_ = [
        ("Status", c_uint16),
        ("Area", ApiHalAreaType),
        ("Address", c_uint32),
        ("Length", c_uint16),
    ]

    def __init__(self, status: int, area: ApiHalAreaType, address: int, length: int):
        self.Primitive = Commands.API_HAL_WRITE_CFM
        self.Status = status
        self.Area = area
        self.Address = address
        self.Length = length

from enum import Enum
from ctypes import (
    Structure,
    c_uint8,
    c_uint16,
    c_uint32,
    c_ubyte,
    Array,
    sizeof,
    cast,
    POINTER,
)
from typing import Optional, Type
from .Api import BaseCommand
from .Commands import Commands
from enum import IntEnum


class ApiMmSearchModeType(IntEnum):
    API_MM_CONTINOUS_SEARCH = 0x00
    API_MM_SINGLE_SEARCH = 0x01


class ApiPpMmRegistrationSearchReq(BaseCommand):
    _fields_ = [("SearchMode", c_uint8)]

    def __init__(self, search_mode: ApiMmSearchModeType):
        self.Primitive = Commands.API_PP_MM_REGISTRATION_SEARCH_REQ
        self.SearchMode = search_mode.value


class ApiPpMmRegistrationSearchCfm(BaseCommand):
    _fields_ = [
        ("Rfpi", c_uint8),
        ("FpCapBit24_31", c_uint8),
        ("FpCapBit32_39", c_uint8),
        ("FpCapBit40_47", c_uint8),
    ]

    #   rsuint8 Rfpi[5];                      The RFPI (Radio Fixed Part Identifier) of
    #                                            the found FP
    #   rsuint8 FpCapBit24_31;                bit0: a31 Conference
    #                                            bit1: a30 Permanent CLIR
    #                                            bit2: a29 NG-DECT extended wideband voice
    #                                            bit3-6: a25-a28 DPRS
    #                                            bit7: a24 NG-DECT wideband voice
    #   rsuint8 FpCapBit32_39;                bit0: a39 Reserved
    #                                            bit1: a38 Reserved
    #                                            bit2: a37 Reserved
    #                                            bit3: a36 Reserved
    #                                            bit4: a35 No emission
    #                                            bit5: a34 Multiple lines
    #                                            bit6: a33 Call deflection
    #                                            bit7: a32 Call intrusion
    #   rsuint8 FpCapBit40_47;                bit0: a47 Reserved
    #                                            bit1: a46 Reserved
    #                                            bit2: a45 Light data services
    #                                            bit3: a44 Reserved
    #                                            bit4: a43 Reserved
    #                                            bit5: a42 Early encryption
    #                                            bit6: a41 Reserved
    #                                            bit7: a40 Reserved

    def __init__(
        self,
        rfpi: bytes,
        fp_cap_bit_24_31: int,
        fp_cap_bit_32_39: int,
        fp_cap_bit_40_47: int,
    ):
        self.Primitive = Commands.API_PP_MM_REGISTRATION_SEARCH_REQ
        self.Rfpi = rfpi
        self.FpCapBit24_31 = fp_cap_bit_24_31
        self.FpCapBit32_39 = fp_cap_bit_32_39
        self.FpCapBit40_47 = fp_cap_bit_40_47


class ApiPpMmRegistrationAutoReq(BaseCommand):
    _fields_ = [("SearchMode", c_uint8), ("AccessCode", c_uint8 * 4)]

    def __init__(self, search_mode: int, access_code: bytes):
        self.Primitive = Commands.API_PP_MM_REGISTRATION_SEARCH_REQ
        self.SearchMode = search_mode
        self.AccessCode = (c_uint8 * 4)(*access_code)

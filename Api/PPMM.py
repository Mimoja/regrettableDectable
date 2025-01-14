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

from enum import IntEnum


class ApiMmSearchModeType(IntEnum):
    API_MM_CONTINOUS_SEARCH = 0x00
    API_MM_SINGLE_SEARCH = 0x01


class ApiPpMmRegistrationSearchReq(BaseCommand):
    _fields_ = [("SearchMode", c_uint8)]

    def __init__(self, search_mode: ApiMmSearchModeType):
        self.Primitive = Commands.API_PP_MM_REGISTRATION_SEARCH_REQ
        if type(search_mode) is int:
            self.SearchMode = search_mode
        else:
            self.SearchMode = search_mode.value


class ApiPpMmFpNameInd(BaseCommand):
    _fields_ = [
        ("NameLength", c_uint16),
        ("Name", c_uint8 * 1),  # Placeholder for variable-length field
    ]

    def __init__(self, name: bytes):
        self.Primitive = Commands.API_PP_MM_FP_NAME_IND
        self.NameLength = len(name)
        self.set_array(self.Name, (c_uint8 * self.Length)(*name.encode()))



class ApiPpMmRegistrationSearchInd(BaseCommand):
    _fields_ = [
        ("Rfpi", c_uint8 * 5),
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
        rfpi: int,
        fp_cap_bit_24_31: int,
        fp_cap_bit_32_39: int,
        fp_cap_bit_40_47: int,
    ):
        self.Primitive = Commands.API_PP_MM_REGISTRATION_SEARCH_IND
        self.Rfpi = rfpi
        self.FpCapBit24_31 = fp_cap_bit_24_31
        self.FpCapBit32_39 = fp_cap_bit_32_39
        self.FpCapBit40_47 = fp_cap_bit_40_47

    def caps(self):
        return {
            "Conference": bool(self.FpCapBit24_31 & 0x01),
            "PermanentCLIR": bool(self.FpCapBit24_31 & 0x02),
            "NG_DECT_extended_wideband_voice": bool(self.FpCapBit24_31 & 0x04),
            "DPRS": (self.FpCapBit24_31 >> 3) & 0x0F,
            "NG_DECT_wideband_voice": bool(self.FpCapBit24_31 & 0x80),
            "No_emission": bool(self.FpCapBit32_39 & 0x10),
            "Multiple_lines": bool(self.FpCapBit32_39 & 0x20),
            "Call_deflection": bool(self.FpCapBit32_39 & 0x40),
            "Call_intrusion": bool(self.FpCapBit32_39 & 0x80),
            "Light_data_services": bool(self.FpCapBit40_47 & 0x04),
            "Early_encryption": bool(self.FpCapBit40_47 & 0x20),
        }


class ApiPpMmRegistrationAutoReq(BaseCommand):
    _fields_ = [("SearchMode", c_uint8), ("AccessCode", c_uint8 * 4)]

    def __init__(self, search_mode: int, access_code: bytes):
        self.Primitive = Commands.API_PP_MM_REGISTRATION_SEARCH_REQ
        self.SearchMode = search_mode
        self.AccessCode = (c_uint8 * 4)(*access_code)


class ApiPpMmRegistrationSelectedReq(BaseCommand):
    _fields_ = [
        ("SubscriptionNo", c_uint8),
        ("AcCode", c_uint8 * 4),
        ("Rfpi", c_uint8 * 5),
    ]

    def __init__(self, subscription_no: int, ac_code: bytes, rfpi: bytes):
        self.Primitive = Commands.API_PP_MM_REGISTRATION_SELECTED_REQ
        self.SubscriptionNo = subscription_no
        self.AcCode = (c_uint8 * 4)(*ac_code)
        self.Rfpi = (c_uint8 * 5)(*rfpi)


class ApiPpMmRejectReasonType(IntEnum):
    API_MM_REJ_NO_REASON = 0x00
    API_MM_REJ_TPUI_UNKNOWN = 0x01
    API_MM_REJ_IPUI_UNKNOWN = 0x02
    API_MM_REJ_NETWORK_ASSIGNED_ID_UNKNOWN = 0x03
    API_MM_REJ_IPEI_NOT_ACCEPTED = 0x05
    API_MM_REJ_IPUI_NOT_ACCEPTED = 0x06
    API_MM_REJ_AUTH_FAILED = 0x10
    API_MM_REJ_NO_AUTH_ALGORITHM = 0x11
    API_MM_REJ_AUTH_ALGORITHM_NOT_SUPPORTED = 0x12
    API_MM_REJ_AUTH_KEY_NOT_SUPPORTED = 0x13
    API_MM_REJ_UPI_NOT_ENTERED = 0x14
    API_MM_REJ_NO_CIPHER_ALGORITHM = 0x17
    API_MM_REJ_CIPHER_ALGORITHM_NOT_SUPPORTED = 0x18
    API_MM_REJ_CIPHER_KEY_NOT_SUPPORTED = 0x19
    API_MM_REJ_INCOMPATIBLE_SERVICE = 0x20
    API_MM_REJ_FALSE_LCE_REPLY = 0x21
    API_MM_REJ_LATE_LCE_REPLY = 0x22
    API_MM_REJ_INVALID_TPUI = 0x23
    API_MM_REJ_TPUI_ASSIGN_LIMIT_UNACCEPT = 0x24
    API_MM_REJ_UNSUFFICIENT_MEMORY = 0x2F
    API_MM_REJ_OVERLOAD = 0x30
    API_MM_REJ_TEST_CALL_BACK_NORM_ENBLOC = 0x40
    API_MM_REJ_TEST_CALL_BACK_NORM_PIECEWISE = 0x41
    API_MM_REJ_TEST_CALL_BACK_EMERG_ENBLOC = 0x42
    API_MM_REJ_TEST_CALL_BACK_EMERG_PIECEWISE = 0x43
    API_MM_REJ_INVALID_MESSAGE = 0x5F
    API_MM_REJ_IE_ERROR = 0x60
    API_MM_REJ_INVALID_IE_CONTENTS = 0x64
    API_MM_REJ_TIMER_EXPIRY = 0x70
    API_MM_REJ_PLMN_NOT_ALLOWD = 0x76
    API_MM_REJ_LOCATION_AREA_NOT_ALLOWED = 0x80
    API_MM_REJ_NATIONAL_ROAMING_NOT_ALLOWED = 0x81
    API_MM_REJ_TERMINAL_IN_ACTIVE_CALL = 0x90
    API_MM_REJ_TERMINAL_IN_FWU_CALL = 0x91
    API_MM_REJ_MM_TRANSACTION_ONGOING = 0x92


class ApiPpMmRegistrationFailedInd(BaseCommand):
    _fields_ = [
        ("Reason", c_uint8),
    ]

    def __init__(self, reason: int):
        self.Primitive = Commands.API_PP_MM_REGISTRATION_FAILED_IND
        self.Reason = reason

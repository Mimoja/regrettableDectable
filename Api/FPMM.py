from enum import IntEnum
from ctypes import (
    c_uint8,
)
from .Api import BaseCommand
from .Commands import Commands

# -----------------------------------------------------------------------------
# Enumerations
# -----------------------------------------------------------------------------


class ApiMmRejectReasonType(IntEnum):
    MM_REJ_NO_REJECT_REASON = 0x00
    MM_REJ_TPUI_UNKNOWN = 0x01
    MM_REJ_IPUI_UNKNOWN = 0x02
    MM_REJ_NETWORK_ASSIGNED_ID_UNKNOWN = 0x03
    MM_REJ_IPEI_NOT_ACCEPTED = 0x05
    MM_REJ_IPUI_NOT_ACCEPTED = 0x06
    MM_REJ_AUTH_FAILED = 0x10
    MM_REJ_NO_AUTH_ALGORITHM = 0x11
    MM_REJ_AUTH_ALGORITHM_NOT_SUPPORTED = 0x12
    MM_REJ_AUTH_KEY_NOT_SUPPORTED = 0x13
    MM_REJ_UPI_NOT_ENTERED = 0x14
    MM_REJ_NO_CIPHER_ALGORITHM = 0x17
    MM_REJ_CIPHER_ALGORITHM_NOT_SUPPORTED = 0x18
    MM_REJ_CIPHER_KEY_NOT_SUPPORTED = 0x19
    MM_REJ_INCOMPATIBLE_SERVICE = 0x20
    MM_REJ_FALSE_LCE_REPLY = 0x21
    MM_REJ_LATE_LCE_REPLY = 0x22
    MM_REJ_INVALID_TPUI = 0x23
    MM_REJ_TPUI_ASSIGN_LIMIT_UNACCEPT = 0x24
    MM_REJ_UNSUFFICIENT_MEMORY = 0x2F
    MM_REJ_OVERLOAD = 0x30
    MM_REJ_INVALID_MESSAGE = 0x5F
    MM_REJ_TIMER_EXPIRY = 0x70
    MM_REJ_PLMN_NOT_ALLOWED = 0x76


class ApiMmProtocolPcmSyncType(IntEnum):
    SLAVE = 0x00
    MASTER = 0x01
    SLAVE_1_FS_DELAY = 0x02


class ApiMmRegistrationModeType(IntEnum):
    DISABLED = 0x00
    CONTINUOUS = 0x01
    SINGLE = 0x02


# -----------------------------------------------------------------------------
# Command Definitions
# -----------------------------------------------------------------------------


class ApiFpMmGetIdReq(BaseCommand):

    def __init__(self):
        self.Primitive = Commands.API_FP_MM_GET_ID_REQ


class ApiFpMmGetIdCfm(BaseCommand):
    _fields_ = [("Status", c_uint8), ("Id", c_uint8 * 5)]

    def __init__(self, status: int, id_bytes: bytes):
        self.Primitive = Commands.API_FP_MM_GET_ID_CFM
        self.Status = status
        if len(id_bytes) != 5:
            raise ValueError("Id must be 5 bytes")
        self.Id = (c_uint8 * 5)(*id_bytes)


class ApiFpMmGetAccessCodeReq(BaseCommand):
    def __init__(self):
        self.Primitive = Commands.API_FP_MM_GET_ACCESS_CODE_REQ


class ApiFpMmSetAccessCodeReq(BaseCommand):
    _fields_ = [
        ("Ac", c_uint8 * 4),
    ]

    def __init__(self, access_code: bytes):
        self.Primitive = Commands.API_FP_MM_SET_ACCESS_CODE_REQ
        if len(access_code) != 4:
            raise ValueError("Access code must be 4 bytes")
        self.Ac = (c_uint8 * 4)(*access_code)


class ApiFpMmGetAccessCodeCfm(BaseCommand):
    _fields_ = [("Status", c_uint8), ("Ac", c_uint8 * 4)]

    def __init__(self, status: int, access_code: bytes):
        self.Primitive = Commands.API_FP_MM_GET_ACCESS_CODE_CFM
        self.Status = status
        if len(access_code) != 4:
            raise ValueError("Access code must be 4 bytes")
        self.Ac = (c_uint8 * 4)(*access_code)


class ApiFpMmSetNameReq(BaseCommand):
    _fields_ = [
        ("Length", c_uint8),
        ("Data", c_uint8 * 1),  # Placeholder for dynamic field
    ]

    def __init__(self, name: str):
        self.Primitive = Commands.API_FP_MM_SET_NAME_REQ
        self.Length = len(name)
        self.set_array(self.Data, (c_uint8 * self.Length)(*name.encode()))


class ApiFpMmGetNameCfm(BaseCommand):
    _fields_ = [
        ("Status", c_uint8),
        ("Max", c_uint8),
        ("Length", c_uint8),
        ("Data", c_uint8 * 1),  # Placeholder for dynamic field
    ]

    def __init__(self, status: int, max_len: int, name: str):
        self.Primitive = Commands.API_FP_MM_GET_NAME_CFM
        self.Status = status
        self.Max = max_len
        self.Length = len(name)
        self.set_array(self.Data, (c_uint8 * self.Length)(*name.encode()))


class ApiFpMmGetAccessCodeCfm(BaseCommand):
    _fields_ = [("Status", c_uint8), ("Ac", c_uint8 * 4)]

    def __init__(self, status: int, access_code: bytes):
        self.Primitive = Commands.API_FP_MM_GET_ACCESS_CODE_CFM
        self.Status = status
        if len(access_code) != 4:
            raise ValueError("Access code must be 4 bytes")
        self.Ac = (c_uint8 * 4)(*access_code)

from enum import IntEnum
from .Api import BaseCommand
from .Commands import Commands
from ctypes import c_uint8, c_uint16, c_uint32, Structure

from Api.Api import RsStatusType


class ApiCcBasicServiceType(IntEnum):
    API_BASIC_SPEECH = 0x00
    API_LRMS_SERVICE = 0x05
    API_WIDEBAND_SPEECH = 0x08
    API_LDS_CLASS4 = 0x09
    API_LDS_CLASS3 = 0x0A
    API_BS_OTHER = 0x0F


class ApiCcCallClassType(IntEnum):
    API_CC_LIA_SERVICE = 0x02
    API_CC_MESSAGE = 0x04
    API_CC_NORMAL = 0x08
    API_CC_INTERNAL = 0x09
    API_CC_SERVICE = 0x0B


class ApiCcSignalType(IntEnum):
    API_CC_SIGNAL_DIAL_TONE_ON = 0x00
    API_CC_SIGNAL_RINGBACK_TONE_ON = 0x01
    API_CC_SIGNAL_INTERCEPT_TONE_ON = 0x02
    API_CC_SIGNAL_NETWORK_CONGESTION_TONE_ON = 0x03
    API_CC_SIGNAL_BUSY_TONE_ON = 0x04
    API_CC_SIGNAL_CONFIRM_TONE_ON = 0x05
    API_CC_SIGNAL_ANSWER_TONE_ON = 0x06
    API_CC_SIGNAL_CALL_WAITING_TONE_ON = 0x07
    API_CC_SIGNAL_OFF_HOOK_WARNING_TONE = 0x08
    API_CC_SIGNAL_NEGATIVE_ACKNOWLEDGEMENT = 0x09
    API_CC_SIGNAL_TONES_OFF = 0x3F
    API_CC_SIGNAL_ALERT_ON_PATTERN_0_INT = 0x40
    API_CC_SIGNAL_ALERT_ON_PATTERN_1 = 0x41
    API_CC_SIGNAL_ALERT_ON_PATTERN_2 = 0x42
    API_CC_SIGNAL_ALERT_ON_PATTERN_3 = 0x43
    API_CC_SIGNAL_ALERT_ON_PATTERN_4 = 0x44
    API_CC_SIGNAL_ALERT_ON_PATTERN_5 = 0x45
    API_CC_SIGNAL_ALERT_ON_PATTERN_6 = 0x46
    API_CC_SIGNAL_ALERT_ON_PATTERN_7 = 0x47
    API_CC_SIGNAL_ALERT_ON_CONTINUOUS = 0x48
    API_CC_SIGNAL_ALERT_OFF = 0x4F
    API_CC_SIGNAL_CUSTOM_FIRST = 0x80
    API_CC_SIGNAL_CUSTOM_NONE = 0xFF


class ApiCcProgressIndType(IntEnum):
    API_IN_BAND_AVAILABLE = 0x08
    API_IN_BAND_NOT_AVAILABLE = 0x09
    API_PROGRESS_INVALID = 0xFF


class ApiCcSetupReq(BaseCommand):
    _fields_ = [
        ("ConEi", c_uint16),
        ("BasicService", c_uint8),
        ("CallClass", c_uint8),
        ("InfoElementLength", c_uint16),
        ("InfoElement", c_uint8 * 1),
    ]

    def __init__(
        self,
        con_ei: int,
        service: ApiCcBasicServiceType,
        call_class: ApiCcCallClassType,
        info: bytes,
    ):
        self.Primitive = Commands.API_CC_SETUP_REQ
        self.ConEi = con_ei
        self.BasicService = service
        self.CallClass = call_class
        self.InfoElementLength = len(info)
        self.set_array(self.InfoElement, (c_uint8 * len(info))(*info))


class ApiCcSetupInd(BaseCommand):
    _fields_ = [
        ("ConEi", c_uint16),
        ("BasicService", c_uint8),
        ("CallClass", c_uint8),
        ("Signal", c_uint8),
        ("InfoElementLength", c_uint16),
        ("InfoElement", c_uint8 * 1),
    ]

    def __init__(
        self,
        con_ei: int,
        service: ApiCcBasicServiceType,
        call_class: ApiCcCallClassType,
        signal: ApiCcSignalType,
        info: bytes,
    ):
        self.Primitive = Commands.API_CC_SETUP_REQ
        self.ConEi = con_ei
        self.BasicService = service
        self.CallClass = call_class
        self.Signal = signal
        self.InfoElementLength = len(info)
        self.set_array(self.InfoElement, (c_uint8 * len(info))(*info))


class ApiCcSetupAckInd(BaseCommand):
    _fields_ = [
        ("ConEi", c_uint16),
        ("ProgressInd", c_uint8),
        ("Signal", c_uint8),
        ("InfoElementLength", c_uint16),
        ("InfoElement", c_uint8 * 1),
    ]

    def __init__(
        self,
        con_ei: int,
        progress: ApiCcProgressIndType,
        signal: ApiCcSignalType,
        info: bytes,
    ):
        self.Primitive = Commands.API_CC_SETUP_ACK_IND
        self.ConEi = con_ei
        self.ProgressInd = progress
        self.Signal = signal
        self.InfoElementLength = len(info)
        self.set_array(self.InfoElement, (c_uint8 * len(info))(*info))


class ApiCcProcInd(BaseCommand):
    _fields_ = [
        ("ConEi", c_uint16),
        ("ProgressInd", c_uint8),
        ("Signal", c_uint8),
        ("InfoElementLength", c_uint16),
        ("InfoElement", c_uint8 * 1),
    ]

    def __init__(
        self,
        con_ei: int,
        progress: ApiCcProgressIndType,
        signal: ApiCcSignalType,
        info: bytes,
    ):
        self.Primitive = Commands.API_CC_CALL_PROC_IND
        self.ConEi = con_ei
        self.ProgressInd = progress
        self.Signal = signal
        self.InfoElementLength = len(info)
        self.set_array(self.InfoElement, (c_uint8 * len(info))(*info))


class ApiCcAlertInd(BaseCommand):
    _fields_ = [
        ("ConEi", c_uint16),
        ("ProgressInd", c_uint8),
        ("Signal", c_uint8),
        ("InfoElementLength", c_uint16),
        ("InfoElement", c_uint8 * 1),
    ]

    def __init__(
        self,
        con_ei: int,
        progress: ApiCcProgressIndType,
        signal: ApiCcSignalType,
        info: bytes,
    ):
        self.Primitive = Commands.API_CC_ALERT_IND
        self.ConEi = con_ei
        self.ProgressInd = progress
        self.Signal = signal
        self.InfoElementLength = len(info)
        self.set_array(self.InfoElement, (c_uint8 * len(info))(*info))


class ApiCcConnectInd(BaseCommand):
    _fields_ = [
        ("ConEi", c_uint16),
        ("InfoElementLength", c_uint16),
        ("InfoElement", c_uint8 * 1),
    ]

    def __init__(
        self,
        con_ei: int,
        info: bytes,
    ):
        self.Primitive = Commands.API_CC_CONNECT_IND
        self.ConEi = con_ei
        self.InfoElementLength = len(info)
        self.set_array(self.InfoElement, (c_uint8 * len(info))(*info))


class ApiCcConnectRes(BaseCommand):
    _fields_ = [
        ("ConEi", c_uint16),
        ("InfoElementLength", c_uint16),
        ("InfoElement", c_uint8 * 1),
    ]

    def __init__(
        self,
        con_ei: int,
        info: bytes,
    ):
        self.Primitive = Commands.API_CC_CONNECT_RES
        self.ConEi = con_ei
        self.InfoElementLength = len(info)
        self.set_array(self.InfoElement, (c_uint8 * len(info))(*info))


class ApiCcConnectReq(BaseCommand):
    _fields_ = [
        ("ConEi", c_uint16),
        ("InfoElementLength", c_uint16),
        ("InfoElement", c_uint8 * 1),
    ]

    def __init__(
        self,
        con_ei: int,
        info: bytes,
    ):
        self.Primitive = Commands.API_CC_CONNECT_REQ
        self.ConEi = con_ei
        self.InfoElementLength = len(info)
        self.set_array(self.InfoElement, (c_uint8 * len(info))(*info))


class ApiCcConnectCfm(BaseCommand):
    _fields_ = [
        ("ConEi", c_uint16),
    ]

    def __init__(
        self,
        con_ei: int,
    ):
        self.Primitive = Commands.API_CC_CONNECT_CFM
        self.ConEi = con_ei


class ApiCcAlertReq(BaseCommand):
    _fields_ = [
        ("ConEi", c_uint16),
        ("InfoElementLength", c_uint16),
        ("InfoElement", c_uint8 * 1),
    ]

    def __init__(
        self,
        con_ei: int,
        info: bytes,
    ):
        self.Primitive = Commands.API_CC_ALERT_REQ
        self.ConEi = con_ei
        self.InfoElementLength = len(info)
        self.set_array(self.InfoElement, (c_uint8 * len(info))(*info))


class ApiCcInfoReq(BaseCommand):
    _fields_ = [
        ("ConEi", c_uint16),
        ("InfoElementLength", c_uint16),
        ("InfoElement", c_uint8 * 1),
    ]

    def __init__(
        self,
        con_ei: int,
        info: bytes,
    ):
        self.Primitive = Commands.API_CC_INFO_REQ
        self.ConEi = con_ei
        self.InfoElementLength = len(info)
        self.set_array(self.InfoElement, (c_uint8 * len(info))(*info))


class ApiCcInfoInd(BaseCommand):
    _fields_ = [
        ("ConEi", c_uint16),
        ("ProgressInd", c_uint8),
        ("Signal", c_uint8),
        ("InfoElementLength", c_uint16),
        ("InfoElement", c_uint8 * 1),
    ]

    def __init__(
        self,
        con_ei: int,
        progress: ApiCcProgressIndType,
        signal: ApiCcSignalType,
        info: bytes,
    ):
        self.Primitive = Commands.API_CC_INFO_IND
        self.ConEi = con_ei
        self.ProgressInd = progress
        self.Signal = signal
        self.InfoElementLength = len(info)
        self.set_array(self.InfoElement, (c_uint8 * len(info))(*info))


class ApiCcReleaseReasonType(IntEnum):
    API_RR_NORMAL = 0x00
    API_RR_UNEXPECTED_MESSAGE = 0x01
    API_RR_UNKNOWN_TRANSACTION_ID = 0x02
    API_RR_MANDATORY_IE_MISSING = 0x03
    API_RR_INVALID_IE_CONTENTS = 0x04
    API_RR_INCOMPATIBLE_SERVICE = 0x05
    API_RR_SERVICE_NOT_IMPLEMENTED = 0x06
    API_RR_NEGOTIATION_NOT_SUPPORTED = 0x07
    API_RR_INVALID_IDENTY = 0x08
    API_RR_AUTHEN_FAILED = 0x09
    API_RR_UNKNOWN_IDENTITY = 0x0A
    API_RR_NEGOTIATION_FAILED = 0x0B
    API_RR_TIMER_EXPIRY = 0x0D
    API_RR_PARTIAL_RELEASE = 0x0E
    API_RR_UNKNOWN = 0x0F
    API_RR_USER_DETACHED = 0x10
    API_RR_USER_OUT_RANGE = 0x11
    API_RR_USER_UNKNOWN = 0x12
    API_RR_USER_ACTIVE = 0x13
    API_RR_USER_BUSY = 0x14
    API_RR_USER_REJECTION = 0x15
    API_RR_USER_CALL_MODIFY = 0x16
    API_RR_EXTERNAL_HANDOVER_NOT_SUPPORTED = 0x21
    API_RR_NETWORK_PARAMETERS_MISSING = 0x22
    API_RR_EXTERNAL_HANDOVER_RELEASE = 0x23
    API_RR_OVERLOAD = 0x31
    API_RR_INSUFFICIENT_RESOURCES = 0x32
    API_RR_IWU_CONGESTION = 0x34
    API_RR_CALL_RESTRICTION = 0x40
    API_RR_SECURITY_ATTACK_ASSUMED = 0x40
    API_RR_ENCRYPTION_ACTIVATION_FAILED = 0x41
    API_RR_RE_KEYING_FAILED = 0x42


class ApiCcReleaseReq(BaseCommand):
    _fields_ = [
        ("ConEi", c_uint16),
        ("Reason", c_uint8),
        ("InfoElementLength", c_uint16),
        ("InfoElement", c_uint8 * 1),
    ]

    def __init__(
        self,
        con_ei: int,
        reason: ApiCcReleaseReasonType,
        info: bytes,
    ):
        self.Primitive = Commands.API_CC_RELEASE_REQ
        self.ConEi = con_ei
        self.Reason = reason
        self.InfoElementLength = len(info)
        self.set_array(self.InfoElement, (c_uint8 * len(info))(*info))


class ApiCcReleaseCfm(BaseCommand):
    _fields_ = [
        ("ConEi", c_uint16),
        ("InfoElementLength", c_uint16),
        ("InfoElement", c_uint8 * 1),
    ]

    def __init__(
        self,
        con_ei: int,
        info: bytes,
    ):
        self.Primitive = Commands.API_CC_RELEASE_CFM
        self.ConEi = con_ei
        self.InfoElementLength = len(info)
        self.set_array(self.InfoElement, (c_uint8 * len(info))(*info))


class ApiCcReleaseInd(BaseCommand):
    _fields_ = [
        ("ConEi", c_uint16),
        ("Reason", c_uint8),
        ("InfoElementLength", c_uint16),
        ("InfoElement", c_uint8 * 1),
    ]

    def __init__(
        self,
        con_ei: int,
        reason: ApiCcReleaseReasonType,
        info: bytes,
    ):
        self.Primitive = Commands.API_CC_RELEASE_IND
        self.ConEi = con_ei
        self.Reason = reason
        self.InfoElementLength = len(info)
        self.set_array(self.InfoElement, (c_uint8 * len(info))(*info))


class ApiCcReleaseRes(BaseCommand):
    _fields_ = [
        ("ConEi", c_uint16),
        ("InfoElementLength", c_uint16),
        ("InfoElement", c_uint8 * 1),
    ]

    def __init__(
        self,
        con_ei: int,
        info: bytes,
    ):
        self.Primitive = Commands.API_CC_RELEASE_RES
        self.ConEi = con_ei
        self.InfoElementLength = len(info)
        self.set_array(self.InfoElement, (c_uint8 * len(info))(*info))


class ApiCcRejectInd(BaseCommand):
    _fields_ = [
        ("ConEi", c_uint16),
        ("Reason", c_uint8),
        ("InfoElementLength", c_uint16),
        ("InfoElement", c_uint8 * 1),
    ]

    def __init__(
        self,
        con_ei: int,
        reason: ApiCcReleaseReasonType,
        info: bytes,
    ):
        self.Primitive = Commands.API_CC_REJECT_IND
        self.ConEi = con_ei
        self.Reason = reason
        self.InfoElementLength = len(info)
        self.set_array(self.InfoElement, (c_uint8 * len(info))(*info))


class ApiCcRejectReq(BaseCommand):
    _fields_ = [
        ("ConEi", c_uint16),
        ("Reason", c_uint8),
        ("InfoElementLength", c_uint16),
        ("InfoElement", c_uint8 * 1),
    ]

    def __init__(
        self,
        con_ei: int,
        reason: ApiCcReleaseReasonType,
        info: bytes,
    ):
        self.Primitive = Commands.API_CC_REJECT_REQ
        self.ConEi = con_ei
        self.Reason = reason
        self.InfoElementLength = len(info)
        self.set_array(self.InfoElement, (c_uint8 * len(info))(*info))


class ApiCcGetConEiReq(BaseCommand):
    def __init__(self):
        self.Primitive = Commands.API_CC_GET_CONEI_REQ


class ApiCcGetConEiCfm(BaseCommand):
    def __init__(self):
        self.Primitive = Commands.API_CC_GET_CONEI_CFM


class ApiCcConeiChangeInd(BaseCommand):
    _fields_ = [
        ("ConEi", c_uint16),
        ("NewConEi", c_uint16),
    ]

    def __init__(
        self,
        con_ei: int,
        new_con_ei: int,
    ):
        self.Primitive = Commands.API_CC_CONEI_CHANGE_IND
        self.ConEi = con_ei
        self.NewConEi = new_con_ei


class ApiCcModifyCodecReq(BaseCommand):
    _fields_ = [
        ("ConEi", c_uint16),
        ("InfoElementLength", c_uint16),
        ("InfoElement", c_uint8 * 1),
    ]

    def __init__(
        self,
        con_ei: int,
        info: bytes,
    ):
        self.Primitive = Commands.API_CC_MODIFY_CODEC_REQ
        self.ConEi = con_ei
        self.InfoElementLength = len(info)
        self.set_array(self.InfoElement, (c_uint8 * len(info))(*info))


class ApiCcModifyCodecCfm(BaseCommand):
    _fields_ = [
        ("ConEi", c_uint16),
        ("Status", c_uint8),
    ]

    def __init__(
        self,
        con_ei: int,
        status: RsStatusType,
    ):
        self.Primitive = Commands.API_CC_MODIFY_CODEC_CFM
        self.ConEi = con_ei
        self.Status = status.value


class ApiCcModifyCodecInd(BaseCommand):
    _fields_ = [
        ("ConEi", c_uint16),
        ("InfoElementLength", c_uint16),
        ("InfoElement", c_uint8 * 1),
    ]

    def __init__(
        self,
        con_ei: int,
        info: bytes,
    ):
        self.Primitive = Commands.API_CC_MODIFY_CODEC_IND
        self.ConEi = con_ei
        self.InfoElementLength = len(info)
        self.set_array(self.InfoElement, (c_uint8 * len(info))(*info))


class ApiCcModifyCodecRes(BaseCommand):
    _fields_ = [
        ("ConEi", c_uint16),
        ("Status", c_uint8),
    ]

    def __init__(
        self,
        con_ei: int,
        status: RsStatusType,
    ):
        self.Primitive = Commands.API_CC_MODIFY_CODEC_RES
        self.ConEi = con_ei
        self.Status = status.value

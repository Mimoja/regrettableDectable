from enum import IntEnum
from .Api import BaseCommand, VariableSizeCommand, InfoElementCommand
from .Commands import Commands
from ctypes import c_uint8, c_uint16, c_uint32, Structure

from Api.Api import RsStatusType


class ApiCcBasicServiceType(IntEnum):
    """
    Enumeration of basic service types for DECT calls.
    Defines different types of voice and data services.
    """
    API_BASIC_SPEECH = 0x00
    API_LRMS_SERVICE = 0x05
    API_WIDEBAND_SPEECH = 0x08
    API_LDS_CLASS4 = 0x09
    API_LDS_CLASS3 = 0x0A
    API_BS_OTHER = 0x0F


class ApiCcCallClassType(IntEnum):
    """
    Enumeration of call classes.
    Defines different types of calls like normal, internal, service calls.
    """
    API_CC_LIA_SERVICE = 0x02
    API_CC_MESSAGE = 0x04
    API_CC_NORMAL = 0x08
    API_CC_INTERNAL = 0x09
    API_CC_SERVICE = 0x0B


class ApiCcSignalType(IntEnum):
    """
    Enumeration of call control signals.
    Defines various tones and alert patterns used in call control.
    """
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
    """
    Enumeration of call progress indication types.
    Indicates availability of in-band information.
    """
    API_IN_BAND_AVAILABLE = 0x08
    API_IN_BAND_NOT_AVAILABLE = 0x09
    API_PROGRESS_INVALID = 0xFF


class ApiCcSetupReq(InfoElementCommand):
    """
    Call setup request command.
    Used to initiate a new call with specified service and class.
    """

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
        """
        Initialize call setup request.

        Args:
            con_ei (int): Connection endpoint identifier
            service (ApiCcBasicServiceType): Basic service type for the call
            call_class (ApiCcCallClassType): Class of the call
            info (bytes): Additional information elements
        """
        self.Primitive = Commands.API_CC_SETUP_REQ
        self.ConEi = con_ei
        self.BasicService = service
        self.CallClass = call_class
        self.InfoElementLength = len(info)
        self.set_array(self.InfoElement, (c_uint8 * len(info))(*info))


class ApiCcSetupInd(InfoElementCommand):
    """
    Call setup indication command.
    Indicates an incoming call with its characteristics.
    """

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
        """
        Initialize call setup indication.

        Args:
            con_ei (int): Connection endpoint identifier
            service (ApiCcBasicServiceType): Basic service type for the call
            call_class (ApiCcCallClassType): Class of the call
            signal (ApiCcSignalType): Signal type to be used
            info (bytes): Additional information elements
        """
        self.Primitive = Commands.API_CC_SETUP_REQ
        self.ConEi = con_ei
        self.BasicService = service
        self.CallClass = call_class
        self.Signal = signal
        self.InfoElementLength = len(info)
        self.set_array(self.InfoElement, (c_uint8 * len(info))(*info))


class ApiCcSetupAckInd(InfoElementCommand):
    """
    Call setup acknowledgment indication command.
    Indicates acknowledgment of call setup with progress information.
    """

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
        """
        Initialize setup acknowledgment indication.

        Args:
            con_ei (int): Connection endpoint identifier
            progress (ApiCcProgressIndType): Progress indication type
            signal (ApiCcSignalType): Signal type to be used
            info (bytes): Additional information elements
        """
        self.Primitive = Commands.API_CC_SETUP_ACK_IND
        self.ConEi = con_ei
        self.ProgressInd = progress
        self.Signal = signal
        self.InfoElementLength = len(info)
        self.set_array(self.InfoElement, (c_uint8 * len(info))(*info))


class ApiCcProcInd(InfoElementCommand):
    """
    Call proceeding indication command.
    Indicates that call establishment has been initiated.
    """

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
        """
        Initialize call proceeding indication.

        Args:
            con_ei (int): Connection endpoint identifier
            progress (ApiCcProgressIndType): Progress indication type
            signal (ApiCcSignalType): Signal type to be used
            info (bytes): Additional information elements
        """
        self.Primitive = Commands.API_CC_CALL_PROC_IND
        self.ConEi = con_ei
        self.ProgressInd = progress
        self.Signal = signal
        self.InfoElementLength = len(info)
        self.set_array(self.InfoElement, (c_uint8 * len(info))(*info))


class ApiCcAlertInd(InfoElementCommand):
    """
    Call alerting indication command.
    Indicates that the called party is being alerted.
    """

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
        """
        Initialize alerting indication.

        Args:
            con_ei (int): Connection endpoint identifier
            progress (ApiCcProgressIndType): Progress indication type
            signal (ApiCcSignalType): Signal type to be used
            info (bytes): Additional information elements
        """
        self.Primitive = Commands.API_CC_ALERT_IND
        self.ConEi = con_ei
        self.ProgressInd = progress
        self.Signal = signal
        self.InfoElementLength = len(info)
        self.set_array(self.InfoElement, (c_uint8 * len(info))(*info))


class ApiCcConnectInd(InfoElementCommand):
    """
    Call connect indication command.
    Indicates that the call has been answered.
    """

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
        """
        Initialize connect indication.

        Args:
            con_ei (int): Connection endpoint identifier
            info (bytes): Additional information elements
        """
        self.Primitive = Commands.API_CC_CONNECT_IND
        self.ConEi = con_ei
        self.InfoElementLength = len(info)
        self.set_array(self.InfoElement, (c_uint8 * len(info))(*info))


class ApiCcConnectRes(InfoElementCommand):
    """
    Call connect response command.
    Responds to a connect indication.
    """

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
        """
        Initialize connect response.

        Args:
            con_ei (int): Connection endpoint identifier
            info (bytes): Additional information elements
        """
        self.Primitive = Commands.API_CC_CONNECT_RES
        self.ConEi = con_ei
        self.InfoElementLength = len(info)
        self.set_array(self.InfoElement, (c_uint8 * len(info))(*info))


class ApiCcConnectReq(InfoElementCommand):
    """
    Call connect request command.
    Requests to establish a connection.
    """

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
        """
        Initialize connect request.

        Args:
            con_ei (int): Connection endpoint identifier
            info (bytes): Additional information elements
        """
        self.Primitive = Commands.API_CC_CONNECT_REQ
        self.ConEi = con_ei
        self.InfoElementLength = len(info)
        self.set_array(self.InfoElement, (c_uint8 * len(info))(*info))


class ApiCcConnectCfm(BaseCommand):
    """
    Call connect confirmation command.
    Confirms successful connection establishment.
    """

    _fields_ = [
        ("ConEi", c_uint16),
    ]

    def __init__(
        self,
        con_ei: int,
    ):
        """
        Initialize connect confirmation.

        Args:
            con_ei (int): Connection endpoint identifier
        """
        self.Primitive = Commands.API_CC_CONNECT_CFM
        self.ConEi = con_ei


class ApiCcAlertReq(InfoElementCommand):
    """
    Call alerting request command.
    Requests to start alerting the called party.
    """

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
        """
        Initialize alerting request.

        Args:
            con_ei (int): Connection endpoint identifier
            info (bytes): Additional information elements
        """
        self.Primitive = Commands.API_CC_ALERT_REQ
        self.ConEi = con_ei
        self.InfoElementLength = len(info)
        self.set_array(self.InfoElement, (c_uint8 * len(info))(*info))


class ApiCcInfoReq(InfoElementCommand):
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


class ApiCcInfoInd(InfoElementCommand):
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

    def __str__(self):
        return (
            f"ConEI: {self.ConEi}, "
            f"ProgressInd: {ApiCcProgressIndType(self.ProgressInd).name}, "
            f"Signal: {ApiCcSignalType(self.Signal).name}, "
            f"InfoElement: {[str(i) for i in self.infoElements()]}"
        )


class ApiCcReleaseReasonType(IntEnum):
    """
    Enumeration of call release reason types.
    Defines various reasons for call termination.
    """
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


class ApiCcReleaseReq(InfoElementCommand):
    """
    Call release request command.
    Requests to release an established call.
    """

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
        """
        Initialize release request.

        Args:
            con_ei (int): Connection endpoint identifier
            reason (ApiCcReleaseReasonType): Reason for release
            info (bytes): Additional information elements
        """
        self.Primitive = Commands.API_CC_RELEASE_REQ
        self.ConEi = con_ei
        self.Reason = reason
        self.InfoElementLength = len(info)
        self.set_array(self.InfoElement, (c_uint8 * len(info))(*info))


class ApiCcReleaseCfm(InfoElementCommand):
    """
    Call release confirmation command.
    Confirms successful call release.
    """

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
        """
        Initialize release confirmation.

        Args:
            con_ei (int): Connection endpoint identifier
            info (bytes): Additional information elements
        """
        self.Primitive = Commands.API_CC_RELEASE_CFM
        self.ConEi = con_ei
        self.InfoElementLength = len(info)
        self.set_array(self.InfoElement, (c_uint8 * len(info))(*info))


class ApiCcReleaseInd(InfoElementCommand):
    """
    Call release indication command.
    Indicates that a call has been released.
    """

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
        """
        Initialize release indication.

        Args:
            con_ei (int): Connection endpoint identifier
            reason (ApiCcReleaseReasonType): Reason for release
            info (bytes): Additional information elements
        """
        self.Primitive = Commands.API_CC_RELEASE_IND
        self.ConEi = con_ei
        self.Reason = reason
        self.InfoElementLength = len(info)
        self.set_array(self.InfoElement, (c_uint8 * len(info))(*info))


class ApiCcReleaseRes(InfoElementCommand):
    """
    Call release response command.
    Responds to a release indication.
    """

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
        """
        Initialize release response.

        Args:
            con_ei (int): Connection endpoint identifier
            info (bytes): Additional information elements
        """
        self.Primitive = Commands.API_CC_RELEASE_RES
        self.ConEi = con_ei
        self.InfoElementLength = len(info)
        self.set_array(self.InfoElement, (c_uint8 * len(info))(*info))


class ApiCcRejectInd(InfoElementCommand):
    """
    Call reject indication command.
    Indicates that a call has been rejected.
    """

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
        """
        Initialize reject indication.

        Args:
            con_ei (int): Connection endpoint identifier
            reason (ApiCcReleaseReasonType): Reason for rejection
            info (bytes): Additional information elements
        """
        self.Primitive = Commands.API_CC_REJECT_IND
        self.ConEi = con_ei
        self.Reason = reason
        self.InfoElementLength = len(info)
        self.set_array(self.InfoElement, (c_uint8 * len(info))(*info))


class ApiCcRejectReq(InfoElementCommand):
    """
    Call reject request command.
    Requests to reject an incoming call.
    """

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
        """
        Initialize reject request.

        Args:
            con_ei (int): Connection endpoint identifier
            reason (ApiCcReleaseReasonType): Reason for rejection
            info (bytes): Additional information elements
        """
        self.Primitive = Commands.API_CC_REJECT_REQ
        self.ConEi = con_ei
        self.Reason = reason
        self.InfoElementLength = len(info)
        self.set_array(self.InfoElement, (c_uint8 * len(info))(*info))


class ApiCcGetConEiReq(BaseCommand):
    """
    Get connection endpoint identifier request command.
    Requests to get a new connection endpoint identifier.
    """

    def __init__(self):
        """Initialize get connection endpoint identifier request."""
        self.Primitive = Commands.API_CC_GET_CONEI_REQ


class ApiCcGetConEiCfm(BaseCommand):
    """
    Get connection endpoint identifier confirmation command.
    Confirms allocation of a new connection endpoint identifier.
    """

    def __init__(self):
        """Initialize get connection endpoint identifier confirmation."""
        self.Primitive = Commands.API_CC_GET_CONEI_CFM


class ApiCcConeiChangeInd(BaseCommand):
    """
    Connection endpoint identifier change indication command.
    Indicates a change in the connection endpoint identifier.
    """

    _fields_ = [
        ("ConEi", c_uint16),
        ("NewConEi", c_uint16),
    ]

    def __init__(
        self,
        con_ei: int,
        new_con_ei: int,
    ):
        """
        Initialize connection endpoint identifier change indication.

        Args:
            con_ei (int): Current connection endpoint identifier
            new_con_ei (int): New connection endpoint identifier
        """
        self.Primitive = Commands.API_CC_CONEI_CHANGE_IND
        self.ConEi = con_ei
        self.NewConEi = new_con_ei


class ApiCcModifyCodecReq(InfoElementCommand):
    """
    Modify codec request command.
    Requests to modify the codec settings for an active call.
    """

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
        """
        Initialize modify codec request.

        Args:
            con_ei (int): Connection endpoint identifier
            info (bytes): Additional information elements with codec settings
        """
        self.Primitive = Commands.API_CC_MODIFY_CODEC_REQ
        self.ConEi = con_ei
        self.InfoElementLength = len(info)
        self.set_array(self.InfoElement, (c_uint8 * len(info))(*info))


class ApiCcModifyCodecCfm(BaseCommand):
    """
    Modify codec confirmation command.
    Confirms modification of codec settings.
    """

    _fields_ = [
        ("ConEi", c_uint16),
        ("Status", c_uint8),
    ]

    def __init__(
        self,
        con_ei: int,
        status: RsStatusType,
    ):
        """
        Initialize modify codec confirmation.

        Args:
            con_ei (int): Connection endpoint identifier
            status (RsStatusType): Status of the modification request
        """
        self.Primitive = Commands.API_CC_MODIFY_CODEC_CFM
        self.ConEi = con_ei
        self.Status = status.value


class ApiCcModifyCodecInd(InfoElementCommand):
    """
    Modify codec indication command.
    Indicates a request to modify codec settings.
    """

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
        """
        Initialize modify codec indication.

        Args:
            con_ei (int): Connection endpoint identifier
            info (bytes): Additional information elements with codec settings
        """
        self.Primitive = Commands.API_CC_MODIFY_CODEC_IND
        self.ConEi = con_ei
        self.InfoElementLength = len(info)
        self.set_array(self.InfoElement, (c_uint8 * len(info))(*info))


class ApiCcModifyCodecRes(BaseCommand):
    """
    Modify codec response command.
    Responds to a codec modification request.
    """

    _fields_ = [
        ("ConEi", c_uint16),
        ("Status", c_uint8),
    ]

    def __init__(
        self,
        con_ei: int,
        status: RsStatusType,
    ):
        """
        Initialize modify codec response.

        Args:
            con_ei (int): Connection endpoint identifier
            status (RsStatusType): Status of the modification response
        """
        self.Primitive = Commands.API_CC_MODIFY_CODEC_RES
        self.ConEi = con_ei
        self.Status = status.value

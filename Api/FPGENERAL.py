from .Api import BaseCommand, InfoElementCommand
from .Commands import Commands
from ctypes import c_uint8, c_uint16, c_uint32, Structure


# -----------------------------------------------------------------------------
# Command Definitions
# -----------------------------------------------------------------------------


class ApiFpResetReq(BaseCommand):

    def __init__(self):
        self.Primitive = Commands.API_FP_RESET_REQ


class ApiFpResetInd(BaseCommand):

    _fields_ = [
        ("Status", c_uint8),
    ]

    def __init__(self, status: int):
        self.Primitive = Commands.API_FP_RESET_IND
        self.Status = status


class ApiFpGetFwVersionReq(BaseCommand):

    def __init__(self):
        self.Primitive = Commands.API_FP_GET_FW_VERSION_REQ


class ApiFpGetFwVersionCfm(InfoElementCommand):

    _fields_ = [
        ("Status", c_uint8),
        ("VersionHex", c_uint32),
        ("LinkDate", c_uint8 * 5),
        ("DectType", c_uint8),  # Placeholder for ApiDectTypeType
        ("InfoElementLength", c_uint16),
        ("InfoElement", c_uint8 * 1),  # Placeholder for variable-length field
    ]

    def __init__(self, status: int, version_hex: int, link_date: bytes, dect_type: int):
        self.Primitive = Commands.API_FP_GET_FW_VERSION_CFM
        self.Status = status
        self.VersionHex = version_hex
        if len(link_date) != 5:
            raise ValueError("LinkDate must be 5 bytes")
        self.LinkDate = (c_uint8 * 5)(*link_date)
        self.DectType = dect_type
        self.InfoElementLength = 0
        self.InfoElement = (c_uint8 * 1)()

    def set_info_element(self, info_element: bytes):
        """Set the optional InfoElement."""
        self.InfoElementLength = len(info_element)
        self.InfoElement = (c_uint8 * len(info_element))(*info_element)


class ApiFpSetCradleStatusReq(BaseCommand):

    _fields_ = [
        ("ApiCradleStatus", c_uint8),  # Placeholder for ApiCradleStatusType
    ]

    def __init__(self, cradle_status: int):
        self.Primitive = Commands.API_FP_SET_CRADLE_STATUS_REQ
        self.ApiCradleStatus = cradle_status


class ApiFpCradleDetectReq(BaseCommand):

    def __init__(self):
        self.Primitive = Commands.API_FP_CRADLE_DETECT_REQ


class ApiTimeDateCodeType(Structure):
    """
    AI BULLSHIT WARNING!
    The below comment was hallucinated by a brainless machine, do NOT trust it.
    Please remove this Warning upon review / verification of correctness.

    Structure for time and date information.
    Contains fields for year, month, day, hour, minute, second and timezone.
    """
    _pack_ = 1
    _fields_ = [
        ("Year", c_uint8),  # Year since 1900
        ("Month", c_uint8),  # Month 1..12
        ("Day", c_uint8),  # Day 1..31
        ("Hour", c_uint8),  # Hour 0..23
        ("Minute", c_uint8),  # Minute 1..59
        ("Second", c_uint8),  # Second 1..59
        ("TimeZone", c_uint8),  # The Time Zone indicates the difference,
        #                         expressed in quarters of an hour, between the
        #                         local time and GMT. In the first of the two
        #                         semi-octets, the first bit represents the
        #                         algebraic sign of this difference (0: positive;
        #                         1: negative).
        #                         The Time Zone code enables the receiver to
        #                         calculate the equivalent time in GMT from the
        #                         other semi-octets in the element, or indicate the
        #                         time zone (GMT, GMT+1H, etc.), or perform other
        #                         similar calculations as required by the
        #                         implementation.
    ]

    def __init__(
        self,
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        second: int,
        time_zone: int,
    ):
        self.Year = year
        self.Month = month
        self.Day = day
        self.Hour = hour
        self.Minute = minute
        self.Second = second
        self.TimeZone = time_zone


class ApiFpSetTimeReq(BaseCommand):

    _fields_ = [
        ("Coding", c_uint8),  # Placeholder for ApiTimeDateCodingType
        ("Interpretation", c_uint8),  # Placeholder for ApiTimeDateInterpretationType
        ("ApiTimeDateCode", ApiTimeDateCodeType),
    ]

    def __init__(
        self, coding: int, interpretation: int, time_date_code: ApiTimeDateCodeType
    ):
        self.Primitive = Commands.API_FP_SET_TIME_REQ
        self.Coding = coding
        self.Interpretation = interpretation
        self.ApiTimeDateCode = time_date_code


class ApiFpGetTimeReq(BaseCommand):

    def __init__(self):
        self.Primitive = Commands.API_FP_GET_TIME_REQ


class ApiFpSyncTimeReq(BaseCommand):

    _fields_ = [
        ("TerminalId", c_uint16),
    ]

    def __init__(self, terminal_id: int):
        self.Primitive = Commands.API_FP_SYNC_TIME_REQ
        self.TerminalId = terminal_id


class ApiFpSetFeaturesReq(BaseCommand):
    _fields_ = [
        ("ApiFpFeature", c_uint8),
    ]

    def __init__(self, features: int):
        self.Primitive = Commands.API_FP_SET_FEATURES_REQ
        self.ApiFpFeature = features


class ApiFpGetFeaturesReq(BaseCommand):

    def __init__(self):
        self.Primitive = Commands.API_FP_GET_FEATURES_REQ


class ApiFpGetFeaturesCfm(BaseCommand):
    _fields_ = [
        ("CurrentFeatures", c_uint8),
        ("AvailableFeatures", c_uint8),
    ]

    def __init__(self, current_features: int, available_features: int):
        self.Primitive = Commands.API_FP_GET_FEATURES_CFM
        self.CurrentFeatures = current_features
        self.AvailableFeatures = available_features

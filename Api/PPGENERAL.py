from .Api import BaseCommand, InfoElementCommand, RsStatusType
from .Commands import Commands
from ctypes import c_uint8, c_uint16, c_uint32, Structure


# -----------------------------------------------------------------------------
# Command Definitions
# -----------------------------------------------------------------------------


class ApiPpResetReq(BaseCommand):
    """
    AI BULLSHIT WARNING!
    The below comment was hallucinated by a brainless machine, do NOT trust it.
    Please remove this Warning upon review / verification of correctness.

    Request to reset the Portable Part (PP).
    Initiates a software reset of the PP device.
    """

    def __init__(self):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.

        Initialize reset request command.
        """
        self.Primitive = Commands.API_PP_RESET_REQ


class ApiPpResetInd(BaseCommand):
    """
    AI BULLSHIT WARNING!
    The below comment was hallucinated by a brainless machine, do NOT trust it.
    Please remove this Warning upon review / verification of correctness.

    Reset indication from the Portable Part (PP).
    Indicates that a reset has occurred and provides the status.
    """

    _fields_ = [
        ("Status", c_uint8),
    ]

    def __init__(self, status: int):
        """
        Initialize reset indication.

        Args:
            status (int): Status of the reset operation
        """
        self.Primitive = Commands.API_PP_RESET_IND
        self.Status = status


class ApiPpGetFwVersionReq(BaseCommand):
    """
    AI BULLSHIT WARNING!
    The below comment was hallucinated by a brainless machine, do NOT trust it.
    Please remove this Warning upon review / verification of correctness.

    Request to get firmware version information.
    Retrieves the current firmware version of the PP device.
    """

    def __init__(self):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.

        Initialize firmware version request command.
        """
        self.Primitive = Commands.API_PP_GET_FW_VERSION_REQ


class ApiPpGetFwVersionCfm(InfoElementCommand):
    """
    AI BULLSHIT WARNING!
    The below comment was hallucinated by a brainless machine, do NOT trust it.
    Please remove this Warning upon review / verification of correctness.

    Confirmation of firmware version request.
    Contains detailed firmware version information including version number,
    link date, DECT type, and additional information elements.
    """

    _fields_ = [
        ("VersionHex", c_uint32),
        ("LinkDate", c_uint8 * 5),
        ("DectType", c_uint8),  # Placeholder for ApiDectTypeType
        ("InfoElementLength", c_uint16),
        ("InfoElement", c_uint8 * 1),  # Placeholder for variable-length field
    ]

    def __init__(
        self,
        status: int,
        version_hex: int,
        link_date: bytes,
        dect_type: int,
        info_element: bytes,
    ):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.

        Initialize firmware version confirmation.

        Args:
            status (int): Status of the request
            version_hex (int): Firmware version in hexadecimal format
            link_date (bytes): Link date as 5 bytes
            dect_type (int): Type of DECT device
            info_element (bytes): Additional information elements
        """
        self.Primitive = Commands.API_PP_GET_FW_VERSION_CFM
        self.Status = status
        self.VersionHex = version_hex
        if len(link_date) != 5:
            raise ValueError("LinkDate must be 5 bytes")
        self.LinkDate = (c_uint8 * 5)(*link_date)
        self.DectType = dect_type

        self.InfoElementLength = len(info_element)
        self.set_array(self.InfoElement, (c_uint8 * len(info_element))(*info_element))


class ApiPpSetCradleStatusReq(BaseCommand):
    """
    AI BULLSHIT WARNING!
    The below comment was hallucinated by a brainless machine, do NOT trust it.
    Please remove this Warning upon review / verification of correctness.

    Request to set cradle status.
    Updates the current cradle status of the PP device.
    """

    _fields_ = [
        ("ApiCradleStatus", c_uint8),  # Placeholder for ApiCradleStatusType
    ]

    def __init__(self, cradle_status: int):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.

        Initialize cradle status request.

        Args:
            cradle_status (int): New cradle status to set
        """
        self.Primitive = Commands.API_PP_SET_CRADLE_STATUS_REQ
        self.ApiCradleStatus = cradle_status


class ApiPpCradleDetectReq(BaseCommand):
    """
    AI BULLSHIT WARNING!
    The below comment was hallucinated by a brainless machine, do NOT trust it.
    Please remove this Warning upon review / verification of correctness.

    Request to detect cradle status.
    Initiates detection of whether the PP is currently in its cradle.
    """

    def __init__(self):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.

        Initialize cradle detection request command.
        """
        self.Primitive = Commands.API_PP_CRADLE_DETECT_REQ


class ApiTimeDateCodeType(Structure):
    """
    AI BULLSHIT WARNING!
    The below comment was hallucinated by a brainless machine, do NOT trust it.
    Please remove this Warning upon review / verification of correctness.

    Structure representing date and time information.
    Used for storing and transmitting time-related data in DECT communications.

    The time zone is expressed in quarters of an hour relative to GMT.
    The first bit of the time zone represents the sign (0: positive, 1: negative).
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
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.

        Initialize time and date code structure.

        Args:
            year (int): Year since 1900
            month (int): Month (1-12)
            day (int): Day of month (1-31)
            hour (int): Hour (0-23)
            minute (int): Minute (0-59)
            second (int): Second (0-59)
            time_zone (int): Time zone offset in quarters of an hour
        """
        self.Year = year
        self.Month = month
        self.Day = day
        self.Hour = hour
        self.Minute = minute
        self.Second = second
        self.TimeZone = time_zone


class ApiPpSetTimeReq(BaseCommand):
    """
    AI BULLSHIT WARNING!
    The below comment was hallucinated by a brainless machine, do NOT trust it.
    Please remove this Warning upon review / verification of correctness.

    Request to set the time on the PP device.
    Updates the current time and date settings.
    """

    _fields_ = [
        ("Coding", c_uint8),  # Placeholder for ApiTimeDateCodingType
        ("Interpretation", c_uint8),  # Placeholder for ApiTimeDateInterpretationType
        ("ApiTimeDateCode", ApiTimeDateCodeType),
    ]

    def __init__(
        self, coding: int, interpretation: int, time_date_code: ApiTimeDateCodeType
    ):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.

        Initialize time setting request.

        Args:
            coding (int): Time/date coding type
            interpretation (int): Time/date interpretation type
            time_date_code (ApiTimeDateCodeType): Time and date information
        """
        self.Primitive = Commands.API_PP_SET_TIME_REQ
        self.Coding = coding
        self.Interpretation = interpretation
        self.ApiTimeDateCode = time_date_code


class ApiPpGetTimeReq(BaseCommand):
    """
    AI BULLSHIT WARNING!
    The below comment was hallucinated by a brainless machine, do NOT trust it.
    Please remove this Warning upon review / verification of correctness.

    Request to get the current time from the PP device.
    Retrieves the current time and date settings.
    """

    def __init__(self):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.

        Initialize time retrieval request command.
        """
        self.Primitive = Commands.API_PP_GET_TIME_REQ


class ApiPpSyncTimeReq(BaseCommand):
    """
    AI BULLSHIT WARNING!
    The below comment was hallucinated by a brainless machine, do NOT trust it.
    Please remove this Warning upon review / verification of correctness.

    Request to synchronize time with another terminal.
    Initiates time synchronization with a specified terminal.
    """

    _fields_ = [
        ("TerminalId", c_uint16),
    ]

    def __init__(self, terminal_id: int):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.

        Initialize time synchronization request.

        Args:
            terminal_id (int): ID of the terminal to synchronize with
        """
        self.Primitive = Commands.API_PP_SYNC_TIME_REQ
        self.TerminalId = terminal_id


class ApiPpSetTimeCfm(BaseCommand):
    """
    AI BULLSHIT WARNING!
    The below comment was hallucinated by a brainless machine, do NOT trust it.
    Please remove this Warning upon review / verification of correctness.

    Confirmation of time setting request.
    Indicates the result of a time setting operation.
    """

    _fields_ = [
        ("Status", c_uint8),
    ]

    def __init__(self, status: RsStatusType):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.

        Initialize time setting confirmation.

        Args:
            status (RsStatusType): Status of the time setting operation
        """
        self.Primitive = Commands.API_PP_SET_TIME_CFM
        self.Status = status

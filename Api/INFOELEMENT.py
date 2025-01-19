from enum import IntEnum
from termcolor import colored
from struct import unpack, pack, pack_into


class InfoElements(IntEnum):
    """
    AI BULLSHIT WARNING!
    The below comment was hallucinated by a brainless machine, do NOT trust it.
    Please remove this Warning upon review / verification of correctness.

    Enumeration of DECT Information Element types.
    Defines all possible information elements that can be exchanged in DECT messages.
    """
    API_IE_CODEC_LIST = 0x0001
    API_IE_MULTIKEYPAD = 0x0002
    API_IE_MULTI_DISPLAY = 0x0003
    API_IE_CALLED_NUMBER = 0x0004
    API_IE_CALLING_PARTY_NUMBER = 0x0005
    API_IE_CALLING_PARTY_NAME = 0x0006
    API_IE_RELEASE_EXT_REASON = 0x0007
    API_IE_IWU_TO_IWU = 0x0008
    API_IE_PROPRIETARY = 0x0009
    API_IE_UNITDATA = 0x000A
    API_IE_MODEL_ID = 0x000B
    API_IE_LINE_ID = 0x000C
    API_IE_SYSTEM_CALL_ID = 0x000D
    API_IE_AVAILABLE_APIS = 0x000E
    API_IE_AUDIO_DATA_FORMAT = 0x000F
    API_IE_CALL_STATUS = 0x0010
    API_IE_TIME_DATE = 0x0011
    API_IE_PORTABLE_IDENTITY = 0x0012
    API_IE_MMS_GEN_HEADER = 0x0013
    API_IE_MMS_OBJ_HEADER = 0x0014
    API_IE_MMS_EXT_HEADER = 0x0015
    API_IE_SEGMENT_INFO = 0x0016
    API_IE_CALLED_NAME = 0x0017
    API_IE_BASIC_TERMCAPS = 0x0018
    API_IE_TERMCAPS = 0x0019
    API_IE_FACILITY = 0x001A
    API_IE_LOCATION_STATUS = 0x001B
    API_IE_FP_CAPABILITIES = 0x001C
    API_IE_FP_EXTENDED_CAPABILITIES = 0x001D
    API_IE_FP_EXTENDED_CAPABILITIES2 = 0x001E
    API_IE_LAS_SORTING_FIELD_IDENTIFIERS = 0x1001
    API_IE_LAS_EDITABLE_FIELDS = 0x1002
    API_IE_LAS_NON_EDITABLE_FIELDS = 0x1003
    API_IE_LAS_REQUESTED_FIELD_IDENTIFIERS = 0x1004
    API_IE_LAS_SEARCH_TEXT = 0x1005
    API_IE_LAS_LIST_IDENTIFIERS = 0x1006
    API_IE_LAS_NUMBER = 0x1007
    API_IE_LAS_NAME = 0x1008
    API_IE_LAS_DATE_TIME = 0x1009
    API_IE_LAS_ENTRY_READSTATUS = 0x100A
    API_IE_LAS_LINE_NAME = 0x100B
    API_IE_LAS_LINE_ID = 0x100C
    API_IE_LAS_NUMBER_OF_CALLS = 0x100D
    API_IE_LAS_CALL_TYPE = 0x100E
    API_IE_LAS_FIRST_NAME = 0x100F
    API_IE_LAS_CONTACT_NUMBER = 0x1010
    API_IE_LAS_ASS_MELODY = 0x1011
    API_IE_LAS_PIN_CODE = 0x1012
    API_IE_LAS_CLOCK_MASTER = 0x1013
    API_IE_LAS_BASE_RESET = 0x1014
    API_IE_LAS_IP_ADDRESS_TYPE = 0x1015
    API_IE_LAS_IP_ADDRESS = 0x1016
    API_IE_LAS_IP_SUBNET_MASK = 0x1017
    API_IE_LAS_IP_GATEWAY = 0x1018
    API_IE_LAS_IP_DNS = 0x1019
    API_IE_LAS_FIRMWARE_VERSION = 0x101A
    API_IE_LAS_EEPROM_VERSION = 0x101B
    API_IE_LAS_HARDWARE_VERSION = 0x101C
    API_IE_LAS_ATTACHED_HANDSETS = 0x101D
    API_IE_LAS_DIALING_PREFIX = 0x101E
    API_IE_LAS_FP_MELODY = 0x101F
    API_IE_LAS_FP_VOLUME = 0x1020
    API_IE_LAS_BLOCKED_NUMBERS = 0x1021
    API_IE_LAS_MULTIPLE_CALL = 0x1022
    API_IE_LAS_INTRUSION_CALL = 0x1023
    API_IE_LAS_PERMANENT_CLIR = 0x1024
    API_IE_LAS_CALL_FORWARDING_CFU = 0x1025
    API_IE_LAS_CALL_FORWARDING_CFNA = 0x1026
    API_IE_LAS_CALL_FORWARDING_CFB = 0x1027
    API_IE_LAS_CALL_INTERCEPTION = 0x1028
    API_IE_LAS_EMISSION_MODE = 0x1029
    API_IE_LAS_NEW_PIN_CODE = 0x1030
    API_IE_LAS_COUNTRY_CODE = 0x1031
    API_IE_LAS_IPMAC = 0x1032
    API_IE_LAS_DECT_MODE = 0x1033
    API_IE_LAS_PIN_PROTECTED_FIELDS = 0x1034
    API_IE_LAS_DISABLED_FIELDS = 0x1035
    API_IE_LOCKED_ENTRIES_LIST = 0x1036
    API_IE_RP_BABYMONITOR = 0x2001
    API_IE_RP_CLIP = 0x2002
    API_IE_RP_TAM = 0x2003
    API_IE_AUDIO_EXT_INDEX = 0x3000
    API_IE_AUDIO_EXT_POINTER = 0x3001
    API_IE_AUDIO_EXT_ARRAY = 0x3002
    API_IE_INVALID = 0xFFFF


class InfoElement:
    """
    AI BULLSHIT WARNING!
    The below comment was hallucinated by a brainless machine, do NOT trust it.
    Please remove this Warning upon review / verification of correctness.

    Base class for DECT Information Elements.
    Provides functionality for handling information element data and serialization.
    """

    def __init__(self, type: int, data: bytes):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.

        Initialize an Information Element.

        Args:
            type (int): Information element type identifier
            data (bytes): Raw data content of the element
        """
        self.type = type
        self.data = data

    def to_bytes(self):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.

        Serialize the information element to bytes.

        Returns:
            bytes: Serialized information element including type, length, and data
        """
        data = self.data
        if isinstance(data, list):
            data = bytes(data)
        return (
            self.type.to_bytes(2, byteorder="big")
            + len(self.data).to_bytes(2, byteorder="big")
            + data
        )

    def __str__(self):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.

        Create a string representation of the information element.

        Returns:
            str: String representation including type name, length, and content
        """
        try:
            type_name = InfoElements(self.type).name
        except ValueError:
            type_name = f"Unknown {hex(self.type)}"
        return (
            f"Type: {type_name}, Length: {len(self.data)}, Content: {list(self.data)}"
        )


def parseInfoElements(data: bytes):
    """
    AI BULLSHIT WARNING!
    The below comment was hallucinated by a brainless machine, do NOT trust it.
    Please remove this Warning upon review / verification of correctness.

    Parse a sequence of information elements from bytes.

    Args:
        data (bytes): Raw bytes containing one or more information elements

    Returns:
        list: List of parsed InfoElement objects
    """
    elements = []
    while len(data) > 0:
        ie_type = int.from_bytes(data[0:2], byteorder="little")
        ie_length = int.from_bytes(data[2:3], byteorder="little")
        content = data[3 : 3 + ie_length]
        info = InfoElement(ie_type, content)
        elements.append(info)
        data = data[3 + ie_length :]

    return elements


class ApiCodecType(IntEnum):
    """
    AI BULLSHIT WARNING!
    The below comment was hallucinated by a brainless machine, do NOT trust it.
    Please remove this Warning upon review / verification of correctness.

    Enumeration of supported audio codec types.
    Defines codecs with their respective information transfer rates.
    """
    API_CT_NONE = 0x00  # Codec not specified or not relevant.
    API_CT_USER_SPECIFIC_32 = 0x01  # user specific, information transfer rate 32 kbit/s
    API_CT_G726 = 0x02  # G.726 ADPCM, information transfer rate 32 kbit/s
    API_CT_G722 = 0x03  # G.722, information transfer rate 64 kbit/s
    API_CT_G711A = 0x04  # G.711 a-law PCM, information transfer rate 64 kbit/s
    API_CT_G711U = 0x05  # G.711 u-law PCM, information transfer rate 64 kbit/s
    API_CT_G7291 = 0x06  # G.729.1, information transfer rate 32 kbit/s
    API_CT_MP4_32 = 0x07  # MPEG-4 ER AAC-LD, information transfer rate 32 kbit/s
    API_CT_MP4_64 = 0x08  # MPEG-4 ER AAC-LD, information transfer rate 64 kbit/s
    API_CT_USER_SPECIFIC_64 = 0x09  # user specific, information transfer rate 64 kbit/s


class ApiNegotiationIndicatorType(IntEnum):
    """
    AI BULLSHIT WARNING!
    The below comment was hallucinated by a brainless machine, do NOT trust it.
    Please remove this Warning upon review / verification of correctness.

    Enumeration of codec negotiation capabilities.
    Indicates whether codec negotiation is possible.
    """
    API_NI_NOT_POSSIBLE = 0x00
    API_NI_POSSIBLE = 0x01


class ApiMacDlcServiceType(IntEnum):
    """
    AI BULLSHIT WARNING!
    The below comment was hallucinated by a brainless machine, do NOT trust it.
    Please remove this Warning upon review / verification of correctness.

    Enumeration of MAC layer DLC service types.
    Defines different MAC layer service configurations.
    """
    API_MDS_1_MD = 0x00
    API_MDS_1_ND = 0x01
    API_MDS_1_IED = 0x02
    API_MDS_1_IQED = 0x03
    API_MDS_7_ND = 0x04
    API_MDS_1_NDF = 0x05


class ApiCplaneRoutingType(IntEnum):
    """
    AI BULLSHIT WARNING!
    The below comment was hallucinated by a brainless machine, do NOT trust it.
    Please remove this Warning upon review / verification of correctness.

    Enumeration of C-plane routing types.
    Defines different control plane routing configurations.
    """
    API_CPR_CS = 0x00
    API_CPR_CS_CF = 0x01
    API_CPR_CF_CS = 0x02
    API_CPR_CF = 0x03


class ApiSlotSizeType(IntEnum):
    """
    AI BULLSHIT WARNING!
    The below comment was hallucinated by a brainless machine, do NOT trust it.
    Please remove this Warning upon review / verification of correctness.

    Enumeration of DECT slot size types.
    Defines different slot sizes for DECT frame structure.
    """
    API_SS_HS = 0x00
    API_SS_LS640 = 0x01
    API_SS_LS672 = 0x02
    API_SS_FS = 0x04
    API_SS_DS = 0x05


class ApiCodecInfoType:
    """
    AI BULLSHIT WARNING!
    The below comment was hallucinated by a brainless machine, do NOT trust it.
    Please remove this Warning upon review / verification of correctness.

    Class representing codec configuration information.
    Combines codec type with MAC/DLC service, routing, and slot size settings.
    """

    def __init__(
        self,
        codec: ApiCodecType,
        mac_dlc_service: ApiMacDlcServiceType,
        cplane_routing: ApiCplaneRoutingType,
        slot_size: ApiSlotSizeType,
    ):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.

        Initialize codec information.

        Args:
            codec (ApiCodecType): Type of codec to use
            mac_dlc_service (ApiMacDlcServiceType): MAC layer service type
            cplane_routing (ApiCplaneRoutingType): Control plane routing type
            slot_size (ApiSlotSizeType): DECT slot size configuration
        """
        self.codec = codec
        self.mac_dlc_service = mac_dlc_service
        self.cplane_routing = cplane_routing
        self.slot_size = slot_size  #

    @classmethod
    def from_bytes(cls, data):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.

        Create codec information from bytes.

        Args:
            data (bytes): Raw bytes containing codec information

        Returns:
            ApiCodecInfoType: New codec information instance
        """
        codec, mac_dlc_service, cplane_routing, slot_size = unpack("<BBBB", data[:4])
        return cls(codec, mac_dlc_service, cplane_routing, slot_size)

    def to_bytes(self):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.

        Serialize codec information to bytes.

        Returns:
            bytes: Serialized codec information
        """
        return pack(
            "<BBBB",
            self.codec,
            self.mac_dlc_service,
            self.cplane_routing,
            self.slot_size,
        )

    def __str__(self):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.

        Create a string representation of codec information.

        Returns:
            str: String representation with all codec settings
        """
        return f"Codec: {ApiCodecType(self.codec).name}, MacDlcService: {ApiMacDlcServiceType(self.mac_dlc_service).name}, CplaneRouting: {ApiCplaneRoutingType(self.cplane_routing).name}, SlotSize: {ApiSlotSizeType(self.slot_size).name}"


class ApiCodecListType(InfoElement):
    """
    AI BULLSHIT WARNING!
    The below comment was hallucinated by a brainless machine, do NOT trust it.
    Please remove this Warning upon review / verification of correctness.

    Information element containing a list of supported codecs.
    Includes negotiation capability and codec configurations.
    """

    def __init__(
        self,
        negotiation_indicator: ApiNegotiationIndicatorType,
        codecs: ApiCodecInfoType,
    ):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.

        Initialize codec list.

        Args:
            negotiation_indicator (ApiNegotiationIndicatorType): Codec negotiation capability
            codecs (ApiCodecInfoType): List of supported codec configurations
        """
        self.type = InfoElements.API_IE_CODEC_LIST
        self.negotiation_indicator = negotiation_indicator
        self.codecs = codecs

    @classmethod
    def from_bytes(cls, data: bytes | list):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.

        Create codec list from bytes.

        Args:
            data (Union[bytes, list]): Raw data containing codec list

        Returns:
            ApiCodecListType: New codec list instance
        """
        if isinstance(data, list):
            data = bytes(data)
        negotiation_indicator, no_of_codecs = unpack("<BB", data[:2])
        codecs = []
        offset = 2
        for _ in range(no_of_codecs):
            codec_info = ApiCodecInfoType.from_bytes(data[offset : offset + 4])
            codecs.append(codec_info)
            offset += 4
        return cls(negotiation_indicator, codecs)  #

    def to_bytes(self):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.

        Serialize codec list to bytes.

        Returns:
            bytes: Serialized codec list information
        """
        res = pack("<BB", self.negotiation_indicator, len(self.codecs))
        for codec in self.codecs:
            res += codec.to_bytes()
        self.data = res
        return super().to_bytes()

    def __str__(self):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.

        Create a string representation of the codec list.

        Returns:
            str: String representation including negotiation indicator and codecs
        """
        codecs_str = ", ".join(str(codec) for codec in self.codecs)
        return f"NegotiationIndicator: {ApiNegotiationIndicatorType(self.negotiation_indicator).name}, Codecs: [{codecs_str}]"


class ApiNumberTypeType(IntEnum):
    """
    AI BULLSHIT WARNING!
    The below comment was hallucinated by a brainless machine, do NOT trust it.
    Please remove this Warning upon review / verification of correctness.

    Enumeration of number types.
    Defines different formats for telephone numbers.
    """
    ANT_UNKNOWN = 0x00  # Unknown
    ANT_INTERNATIONAL = 0x01  # International number
    ANT_NATIONAL = 0x02  # National number
    ANT_NETWORK_SPECIFIC = 0x03  # Network specific number
    ANT_SUBSCRIBER = 0x04  # Subscriber number
    ANT_ABBREVIATED = 0x06  # Abbreviated number
    ANT_INVALID = 0xFF  # Invalid


class ApiNpiType(IntEnum):
    """
    AI BULLSHIT WARNING!
    The below comment was hallucinated by a brainless machine, do NOT trust it.
    Please remove this Warning upon review / verification of correctness.

    Enumeration of Numbering Plan Identification types.
    Defines different numbering plans for addressing.
    """
    ANPI_UNKNOWN = 0x00  # Unknown
    ANPI_E164_ISDN = 0x01  # ISDN/telephony plan ITU-T Recommendations E.164/E.163
    ANPI_X121 = 0x03  # Data plan ITU-T Recommendation X.121
    ANPI_TCP_IP = 0x07  # TCP/IP address
    ANPI_NATIONAL = 0x08  # National standard plan
    ANPI_PRIVATE = 0x09  # Private plan
    ANPI_SIP = 0x0A  # SIP addressing scheme, To: or From: field (see RFC 3261)
    ANPI_INTERNET = 0x0B  # Internet character format address
    ANPI_LAN_MAC = 0x0C  # LAN MAC address
    ANPI_X400 = 0x0D  # ITU-T Recommendation X.400 [63] address
    ANPI_PROFILE_SERVICE = 0x0E  # Profile service specific alphanumeric identifier
    ANPI_INVALID = 0xFF  # Invalid


class ApiPresentationIndicatorType(IntEnum):
    """
    AI BULLSHIT WARNING!
    The below comment was hallucinated by a brainless machine, do NOT trust it.
    Please remove this Warning upon review / verification of correctness.

    Enumeration of presentation indicator types.
    Defines whether caller information can be displayed.
    """
    API_PRESENTATION_ALLOWED = 0x00  # Presentation allowed.
    API_PRESENTATION_RESTRICTED = 0x01  # Presentation restricted.
    API_PRESENTATION_NUMBER_NA = 0x02  # Number not available.
    API_PRESENTATION_HANSET_LOCATOR = 0x03  # Used to locate physically handsets (have them ring) f. ex.by pressing a physical or logical button on the FP.
    API_INVALID = 0xFF  # [0x04; 0xFF] is reserved.


class ApiScreeningIndicatorType(IntEnum):
    """
    AI BULLSHIT WARNING!
    The below comment was hallucinated by a brainless machine, do NOT trust it.
    Please remove this Warning upon review / verification of correctness.

    Enumeration of screening indicator types.
    Defines the verification status of caller information.
    """
    API_USER_PROVIDED_NOT_SCREENED = 0x00  # User-provided, not screened.
    API_USER_PROVIDED_VERIFIED_PASSED = 0x01  # User-provided, verified and passed.
    API_USER_PROVIDED_VERIFIED_FAILED = 0x02  # User-provided, verified and failed.
    API_NETWORK_PROVIDED = 0x03  # Network provided.
    API_SCR_INVALID = 0xFF  # [0x04; 0xFF] is reserved.


class ApiCallingPartyNumber(InfoElement):
    """
    AI BULLSHIT WARNING!
    The below comment was hallucinated by a brainless machine, do NOT trust it.
    Please remove this Warning upon review / verification of correctness.

    Information element containing calling party number information.
    Includes number type, format, and presentation settings.
    """

    def __init__(self, number_type, npi, presentation_ind, screening_ind, number):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.

        Initialize calling party number information.

        Args:
            number_type: Type of telephone number
            npi: Numbering plan identification
            presentation_ind: Presentation permission indicator
            screening_ind: Number screening status
            number: The actual telephone number
        """
        self.type = InfoElements.API_IE_CALLING_PARTY_NUMBER
        self.number_type = number_type
        self.npi = npi
        self.presentation_ind = presentation_ind
        self.screening_ind = screening_ind
        self.number = number

    @classmethod
    def from_bytes(cls, data):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.

        Create calling party number information from bytes.

        Args:
            data (bytes): Raw data containing number information

        Returns:
            ApiCallingPartyNumber: New calling party number instance
        """
        number_type = ApiNumberTypeType(data[0])
        npi = ApiNpiType(data[1])
        presentation_ind = ApiPresentationIndicatorType(data[2])
        screening_ind = ApiScreeningIndicatorType(data[3])
        number_length = data[4]
        number = bytes(data[5 : 5 + number_length]).decode("ascii")
        new = cls(number_type, npi, presentation_ind, screening_ind, number)
        new.data = data
        return new

    def __str__(self):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.

        Create a string representation of calling party number information.

        Returns:
            str: String representation including all number attributes
        """
        return (
            f"Number: {self.number}, "
            f"NumberType: {ApiNumberTypeType(self.number_type).name}, "
            f"Npi: {ApiNpiType(self.npi).name}, "
            f"PresentationInd: {ApiPresentationIndicatorType(self.presentation_ind).name}, "
            f"ScreeningInd: {ApiScreeningIndicatorType(self.screening_ind).name}"
        )


class ApiUsedAlphabetType(IntEnum):
    """
    AI BULLSHIT WARNING!
    The below comment was hallucinated by a brainless machine, do NOT trust it.
    Please remove this Warning upon review / verification of correctness.

    Enumeration of character encoding types.
    Defines supported character encodings for names.
    """
    AUA_DECT = 0x00  # IA5 chars used.
    AUA_UTF8 = 0x01  # UTF-8 chars used.
    AUA_NETWORK_SPECIFIC = 0xFF


class ApiCallingPartyName(InfoElement):
    """
    AI BULLSHIT WARNING!
    The below comment was hallucinated by a brainless machine, do NOT trust it.
    Please remove this Warning upon review / verification of correctness.

    Information element containing calling party name information.
    Includes character encoding and presentation settings.
    """

    def __init__(
        self,
        used_alphabet: ApiUsedAlphabetType,
        presentation_ind,
        screening_ind,
        name,
    ):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.

        Initialize calling party name information.

        Args:
            used_alphabet (ApiUsedAlphabetType): Character encoding used
            presentation_ind: Presentation permission indicator
            screening_ind: Name screening status
            name: The actual caller name
        """
        self.type = InfoElements.API_IE_CALLING_PARTY_NAME
        self.used_alphabet = used_alphabet
        self.presentation_ind = presentation_ind
        self.screening_ind = screening_ind
        self.name = name

    @classmethod
    def from_bytes(cls, data):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.

        Create calling party name information from bytes.

        Args:
            data (bytes): Raw data containing name information

        Returns:
            ApiCallingPartyName: New calling party name instance
        """
        used_alphabet = ApiNumberTypeType(data[0])
        presentation_ind = ApiPresentationIndicatorType(data[1])
        screening_ind = ApiScreeningIndicatorType(data[2])
        name = data[3:].decode("utf-8")
        return cls(used_alphabet, presentation_ind, screening_ind, name)

    def __str__(self):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.

        Create a string representation of calling party name information.

        Returns:
            str: String representation including all name attributes
        """
        return (
            f"Name: {self.name}, "
            f"Alphabet: {ApiUsedAlphabetType(self.used_alphabet).name}, "
            f"Presentation: {ApiPresentationIndicatorType(self.presentation_ind).name}, "
            f"Screening: {ApiScreeningIndicatorType(self.screening_ind).name}"
        )

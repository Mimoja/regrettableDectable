from ctypes import (
    POINTER,
    Structure,
    c_uint16,
    cast,
    sizeof,
)
import ctypes
import datetime

from enum import Enum, auto, IntEnum
from Api.INFOELEMENT import parseInfoElements


class RsStatusType(IntEnum):
    """
    AI BULLSHIT WARNING!
    The below comment was hallucinated by a brainless machine, do NOT trust it.
    Please remove this Warning upon review / verification of correctness.

    Enumeration of response status types for DECT API commands.
    Defines all possible status codes that can be returned by the DECT device.
    """
    RSS_SUCCESS = 0x00  # The request completed successfully.
    RSS_NOT_SUPPORTED = 0x01  # The request is not supported.
    RSS_BAD_ARGUMENTS = 0x02  # One or more arguments are not correct.
    RSS_BAD_ADDRESS = 0x03  # The address is incorrect.
    RSS_BAD_FUNCTION = 0x04  # Incorrect function.
    RSS_BAD_HANDLE = 0x05  # The handle is invalid.
    RSS_BAD_DATA = 0x06  # The data is invalid.
    RSS_BAD_LENGTH = (
        0x07  # The program issued a command but the command length is incorrect.
    )
    RSS_NO_MEMORY = 0x08  # Not enough storage is available to process this command.
    RSS_NO_DEVICE = 0x09  # No such device.
    RSS_NO_DATA = 0x0A  # No data is available.
    RSS_RETRY = (
        0x0B  # The operation could not be completed. A retry should be performed.
    )
    RSS_NOT_READY = 0x0C  # The device is not ready.
    RSS_IO = 0x0D  # I/O error.
    RSS_CRC = 0x0E  # Data error (cyclic redundancy check).
    RSS_CANCELLED = 0x0F  # The operation was cancelled.
    RSS_RESET = 0x10  # The I/O bus was reset.
    RSS_PENDING = 0x11  # The operation is in progress.
    RSS_BUSY = 0x12  # Device or resource busy.
    RSS_TIMEOUT = 0x13  # This operation returned because the timeout period expired.
    RSS_OVERFLOW = 0x14  # Value too large for defined data type.
    RSS_NOT_FOUND = 0x15  # Element not found.
    RSS_STALLED = 0x16  # Endpoint stalled.
    RSS_DENIED = 0x17  # Access denied or authentication failed.
    RSS_REJECTED = 0x18  # Rejected (e.g., by user).
    RSS_AMBIGUOUS = 0x19  # Ambiguous e.g., name or number.
    RSS_NO_RESOURCE = (
        0x1A  # Not enough resources are available to process this command.
    )
    RSS_NOT_CONNECTED = 0x1B  # No connection to destination.
    RSS_OFFLINE = 0x1C  # Destination is offline.
    RSS_REMOTE_ERROR = 0x1D  # Failed at remote destination.
    RSS_NO_CAPABILITY = 0x1E  # A required capability is missing.
    RSS_FILE_ACCESS = 0x1F  # File access error.
    RSS_DUPLICATE = (
        0x20  # Duplicate entry e.g., same entry already exists when trying to create.
    )
    RSS_LOGGED_OUT = 0x21  # Operation not possible while logged out.
    RSS_ABNORMAL_TERMINATION = 0x22  # Operation terminated abnormally.
    RSS_FAILED = 0x23  # Operation failed.
    RSS_UNKNOWN = 0x24  # Unknown error.
    RSS_BLOCKED = 0x25  # Destination is blocked.
    RSS_NOT_AUTHORIZED = 0x26  # You are not authorized to perform this operation.
    RSS_PROXY_CONNECT = 0x27  # Could not connect to proxy.
    RSS_INVALID_PASSWORD = 0x28  # Invalid password.
    RSS_FORBIDDEN = 0x29  # Forbidden.
    RSS_MISSING_PARAMETER = 0x2A  # One or more mandatory parameters are missing.
    RSS_SPARE_2B = 0x2B  # Spare.
    RSS_SPARE_2C = 0x2C  # Spare.
    RSS_SPARE_2D = 0x2D  # Spare.
    RSS_SPARE_2E = 0x2E  # Spare.
    RSS_SPARE_2F = 0x2F  # Spare.
    RSS_UNAVAILABLE = 0x30  # Service unavailable.
    RSS_NETWORK = 0x31  # Network error.
    RSS_NO_CREDITS = 0x32  # No credits.
    RSS_LOW_CREDITS = 0x33  # Low credits.
    RSS_MAX = 0xFF  # Maximum value.


class BaseCommand(Structure):
    """
    AI BULLSHIT WARNING!
    The below comment was hallucinated by a brainless machine, do NOT trust it.
    Please remove this Warning upon review / verification of correctness.
    
    Base class for all DECT API commands.
    Provides serialization and deserialization functionality for command structures.

    Attributes:
        Primitive (c_uint16): The opcode/primitive identifier for the command
        _raw_ (bytes): Raw bytes representation of the command
        _last_field_original_end (int): Original end position of the last field
    """

    _pack_ = 1
    _fields_ = [
        ("Primitive", c_uint16),  # The opcode/primitive
    ]

    _raw_ = None
    _last_field_original_end = None

    def to_bytes(self) -> bytes:
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.
    
        Serialize the command to bytes.

        Returns:
            bytes: Serialized command data
        """
        if self._raw_:
            return self._raw_
        return bytes(self)

    def set_array(self, entry, data):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.
    
        Set an array field in the command structure.
        Handles resizing the structure to accommodate variable-length arrays.

        Args:
            entry: Array field to set
            data: Data to set in the array
        """
        # We cannot access data[0] to get the size on zero sized arrays
        # therefore we trust that the single element array is enoug
        size = ctypes.sizeof(entry)

        try:
            size = ctypes.sizeof(data[0])
        except TypeError:
            pass
        except ValueError:
            pass
        except IndexError:
            size = 0

        self._last_field_original_end = ctypes.sizeof(self)

        ctypes.resize(self, ctypes.sizeof(self) + size * (len(data) - 1))
        ctypes.memmove(entry, data, ctypes.sizeof(data))

    @staticmethod
    def _set_size(entry, new_size):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.
    
        Internal method to set the size of a ctypes array.
        Uses low-level memory manipulation to resize arrays.

        Args:
            entry: Array to resize
            new_size: New size for the array

        Returns:
            The resized array
        """
        address = id(entry)
        print(hex(address))
        # the incredibly illegal version
        # 1. get memory offset of b_length field in raw pyobject memory (assuming at least 32 bit)
        _tdata = (ctypes.c_int16 * 0x4ACAFFEE).from_address(0)
        memfield = (ctypes.c_char * 0x100).from_address(id(_tdata))
        _loc = bytes(memfield).find(bytes(ctypes.c_size_t(len(_tdata))))
        assert _loc != -1, "Could not find b_length field"

        # 2. change our size at previously determined offset

        print(hex(address))
        b_size = (ctypes.c_size_t).from_address(
            address + _loc - ctypes.sizeof(ctypes.c_size_t)
        )
        b_length = (ctypes.c_size_t).from_address(address + _loc)
        print(b_length, b_size)

        b_size.value = b_size.value // b_length.value * new_size
        b_length.value = new_size
        print(b_length, b_size)
        # print("sanity check:", len(entry), entry)
        return entry

    @classmethod
    def from_bytes(cls, data: bytes) -> "BaseCommand":
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.
    
        Create a command object from bytes.

        Args:
            data (bytes): Serialized command data

        Returns:
            BaseCommand: New command instance

        Raises:
            ValueError: If data length doesn't match command structure
        """
        if len(data) < sizeof(cls):
            raise ValueError(f"Data too short for {cls.__name__}")
        cmd = cls.from_buffer_copy(data)
        if len(data) > sizeof(cls):
            raise ValueError(
                f"Data too long for {cls.__name__}. Use VariableSizeCommand instead"
            )
        cmd._raw_ = data
        return cmd

    def primitive(self):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.
    
        Get the command's primitive identifier.

        Returns:
            int: The primitive/opcode value
        """
        return self.Primitive

    def to_dict(self):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.
    
        Convert the command to a dictionary representation.
        Handles special cases for array fields and oversized last fields.

        Returns:
            dict: Dictionary containing command fields and values
        """
        # This comes from the baseclass and is sometimes not included therefore
        ret = {"Primitive": hex(self.Primitive)}
        # In case the last field is oversized we need to include it manually
        last_field_name = self._fields_[-1][0]

        for name, _ in self._fields_:
            val = getattr(self, name)
            if isinstance(val, ctypes.Array):
                ret[name] = list(val)
                if name == last_field_name and self._last_field_original_end:
                    ret[name] += self.to_bytes()[self._last_field_original_end :]
            else:
                ret[name] = val

        return ret

    def __str__(self):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.
    
        Create a string representation of the command.
        Converts numeric values to hexadecimal format.

        Returns:
            str: String representation of the command
        """
        formated = self.to_dict()
        # convert integers to hex
        for key, value in formated.items():
            if isinstance(value, int):
                formated[key] = hex(value)
            if isinstance(value, list):
                formated[key] = [hex(x) for x in value]

        # stringify the dict
        return str(formated)

    @staticmethod
    def parseDate(date: bytes | list) -> datetime:
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.
    
        Parse a date from bytes or list format.

        Args:
            date (Union[bytes, list]): Date data to parse

        Returns:
            datetime: Parsed datetime object, or None if parsing fails
        """
        if date is None:
            return None

        if isinstance(date, bytes):
            date = list(date)

        try:
            return datetime.datetime.strptime(
                f"{date[0]:x}/{date[1]:x}/{date[2]:x} {date[3]:x}:{date[4]:x}",
                "%d/%m/%y %H:%M",
            )
        except ValueError:
            return None


class VariableSizeCommand(BaseCommand):
    """
    AI BULLSHIT WARNING!
    The below comment was hallucinated by a brainless machine, do NOT trust it.
    Please remove this Warning upon review / verification of correctness.

    Command class that supports variable-sized data fields.
    Extends BaseCommand with functionality for handling variable-length data.
    """

    def data(self):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.
    
        Get the variable-length data from the command.

        Returns:
            list: List of data values
        """
        length_field_name = self._fields_[-2][0]
        last_field_name = self._fields_[-1][0]

        length = getattr(self, length_field_name)
        if length == 0:
            return []

        val = getattr(self, last_field_name)
        val_size = ctypes.sizeof(val)
        val_class = val[0].__class__
        is_byte_array = "ubyte" in self._fields_[-1][1].__name__ or val_size == 1
        vals = list(val)
        if self._last_field_original_end:
            data_left = self.to_bytes()[self._last_field_original_end :]
            while len(data_left) > 0:
                if is_byte_array:
                    new_val = int(data_left[0])
                else:
                    new_val = val_class.from_buffer_copy(data_left)
                vals.append(new_val)
                data_left = data_left[val_size:]

        return vals

    def data_bytes(self):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.
    
        Get the variable-length data as bytes.

        Returns:
            bytes: Raw data bytes
        """
        return b"".join([bytes(x) for x in self.data()])

    @classmethod
    def from_bytes(cls, data: bytes) -> "VariableSizeCommand":
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.
    
        Create a variable-size command from bytes.

        Args:
            data (bytes): Serialized command data

        Returns:
            VariableSizeCommand: New command instance
        """
        if len(data) < sizeof(cls):
            data += bytes([0])

        cmd = cls.from_buffer_copy(data)
        if len(data) > sizeof(cls):
            cmd._last_field_original_end = ctypes.sizeof(cmd)
            ctypes.resize(cmd, len(data))
        cmd._raw_ = data
        return cmd

    def __str__(self):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.
    
        Create a string representation of the variable-size command.

        Returns:
            str: String representation of the command
        """
        length_field_name = self._fields_[-2][0]
        last_field_name = self._fields_[-1][0]

        formated = self.to_dict()
        # convert integers to hex
        for key, value in formated.items():
            if isinstance(value, int):
                formated[key] = hex(value)
            if isinstance(value, list):
                formated[key] = [hex(x) for x in value]
            if key == last_field_name and formated[length_field_name] == 0:
                formated[key] = []

        # stringify the dict
        return str(formated)


class InfoElementCommand(VariableSizeCommand):
    """
    AI BULLSHIT WARNING!
    The below comment was hallucinated by a brainless machine, do NOT trust it.
    Please remove this Warning upon review / verification of correctness.
    
    Command class that contains information elements.
    Extends VariableSizeCommand with functionality for handling info elements.
    """

    def infoElements(self):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.
    
        Parse and return the information elements contained in the command.

        Returns:
            list: List of parsed information elements
        """
        return parseInfoElements(self.data_bytes())

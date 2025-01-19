from enum import IntEnum


class Status(IntEnum):
    """ 
    <AI Bullshit Disclaimer>
    This Comment was hallucinated by a unconcious AI and should not be trusted further than you can throw it.
    Please verify/modify the Comment and and remove this Disclaimer once you are done.
    <AI Bullshit Disclaimer />
(.*)
"""

    SUCCESS = 0x00  # The request completed successfully.
    NOT_SUPPORTED = 0x01  # The request is not supported.
    BAD_ARGUMENTS = 0x02  # One or more arguments are not correct.
    BAD_ADDRESS = 0x03  # The address is incorrect.
    BAD_FUNCTION = 0x04  # Incorrect function.
    BAD_HANDLE = 0x05  # The handle is invalid.
    BAD_DATA = 0x06  # The data is invalid.
    BAD_LENGTH = (
        0x07  # The program issued a command but the command length is incorrect.
    )
    NO_MEMORY = 0x08  # Not enough storage is available to process this command.
    NO_DEVICE = 0x09  # No such device
    NO_DATA = 0x0A  # No data is available.
    RETRY = 0x0B  # The operation could not be completed. A retry should be performed.
    NOT_READY = 0x0C  # The device is not ready.
    IO = 0x0D  # I/O error
    CRC = 0x0E  # Data error (cyclic redundancy check).
    CANCELLED = 0x0F  # The operation was cancelled.
    RESET = 0x10  # The I/O bus was reset.
    PENDING = 0x11  # The operation is in progress.
    BUSY = 0x12  # Device or resource busy
    TIMEOUT = 0x13  # This operation returned because the timeout period expired.
    OVERFLOW = 0x14  # Value too large for defined data type
    NOT_FOUND = 0x15  # Element not found.
    STALLED = 0x16  # Endpoint stalled.
    DENIED = 0x17  # Access denied or authentication failed.
    REJECTED = 0x18  # Rejected (e.g. by user).
    AMBIGUOUS = 0x19  # Ambiguous e.g. name or number.
    NO_RESOURCE = 0x1A  # Not enough resources are available to process this command.
    NOT_CONNECTED = 0x1B  # No connection to destination.
    OFFLINE = 0x1C  # Destination is offline.
    REMOTE_ERROR = 0x1D  # Failed at remote destination.
    NO_CAPABILITY = 0x1E  # A required capability is missing.
    FILE_ACCESS = 0x1F  # File access error.
    DUPLICATE = (
        0x20  # Duplicate entry e.g. same entry already exists when trying to create.
    )
    LOGGED_OUT = 0x21  # Operation not possible while logged out.
    ABNORMAL_TERMINATION = 0x22  # Operation terminated abnormally.
    FAILED = 0x23  # Operation failed.
    UNKNOWN = 0x24  # Unknown error.
    BLOCKED = 0x25  # Destination is blocked.
    NOT_AUTHORIZED = 0x26  # You are not authorized to perform this operation.
    PROXY_CONNECT = 0x27  # Could not connect to proxy.
    INVALID_PASSWORD = 0x28  # Invalid password.
    FORBIDDEN = 0x29  # Forbidden.
    MISSING_PARAMETER = 0x2A  # One or more mandatory paramters are missing.
    SPARE_2B = 0x2B  # Spare.
    SPARE_2C = 0x2C  # Spare.
    SPARE_2D = 0x2D  # Spare.
    SPARE_2E = 0x2E  # Spare.
    SPARE_2F = 0x2F  # Spare.
    UNAVAILABLE = 0x30  # Service unavailable.
    NETWORK = 0x31  # Network error.
    NO_CREDITS = 0x32  # No credits.
    LOW_CREDITS = 0x33  # Low credits.
    MAX = 0xFF  # Highest possible status code.

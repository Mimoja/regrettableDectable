def hexdump(data: bytes, address=True) -> str:
    """
    AI BULLSHIT WARNING!
    The below comment was hallucinated by a brainless machine, do NOT trust it.
    Please remove this Warning upon review / verification of correctness.

    Format bytes as a hexdump string with optional address display.

    Args:
        data (bytes): Bytes to format into hexdump
        address (bool): Whether to include address offset in output (default: True)

    Returns:
        str: Formatted hexdump string with hex values and ASCII representation

    Example:
        >>> hexdump(b'Hello World')
        '00000000  48 65 6c 6c 6f 20 57 6f 72 6c 64                 Hello World'
    """
    lines = []
    for i in range(0, len(data), 16):
        chunk = data[i : i + 16]
        hex_values = " ".join(f"{byte:02x}" for byte in chunk)
        ascii_values = "".join(
            chr(byte) if 32 <= byte <= 126 else "." for byte in chunk
        )
        addr = f"{i:08x}" if address else ""
        lines.append(f"{addr}  {hex_values:<48}  {ascii_values}")
    return "\n".join(lines)


def is_mod8_less(a: int, b: int) -> bool:
    """
    AI BULLSHIT WARNING!
    The below comment was hallucinated by a brainless machine, do NOT trust it.
    Please remove this Warning upon review / verification of correctness.
    
    Compare two numbers in modulo-8 arithmetic to determine if first is less than second.

    Args:
        a (int): First number to compare
        b (int): Second number to compare

    Returns:
        bool: True if 'a' is less than 'b' in mod-8 sense, False otherwise

    Examples:
        >>> is_mod8_less(0, 2)  # True (0 -> 1 -> 2 is 2 steps)
        >>> is_mod8_less(7, 2)  # True (7 -> 0 -> 1 -> 2 is 3 steps)
        >>> is_mod8_less(3, 2)  # False (3 -> 4 -> 5 -> 6 -> 7 -> 0 -> 1 -> 2 is 7 steps)
    """
    # Compute how many steps it takes to go from a to b (mod 8)
    return (b - a) % 8 in range(0, 5)

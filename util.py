def hexdump(data: bytes, address=True) -> str:
    """
    Format bytes as a hexdump string.
    :param data: Bytes to format
    :return: Hexdump string
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
    Return True if 'a' < 'b' in mod-8 sense.
    Example:
      - is_mod8_less(0, 2) -> True
      - is_mod8_less(7, 2) -> True  (7 -> 0 -> 1 -> 2 is 3 steps, so 7 is effectively before 2 modulo 8)
      - is_mod8_less(3, 2) -> False (3 -> 4 -> 5 -> 6 -> 7 -> 0 -> 1 -> 2 is 7 steps, meaning 3 is after 2 in mod 8)
    """
    # Compute how many steps it takes to go from a to b (mod 8)
    return (b - a) % 8 in range(0, 5)

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

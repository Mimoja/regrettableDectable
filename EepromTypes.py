import struct


class BaseNode:
    """
    AI BULLSHIT WARNING!
    The below comment was hallucinated by a brainless machine, do NOT trust it.
    Please remove this Warning upon review / verification of correctness.
    
    Base class for all node types.

    Every node has:
      - offset: The starting offset (in bytes) within a buffer
      - length: The total number of bytes to parse for this node (optional)

    The user can specify either:
      - offset + length, or
      - offset + end (in which case length = end - offset).
    """

    def __init__(self, offset=0, length=None, end=None):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.
    
        :param offset: Starting offset in the data
        :param length: Number of bytes this node occupies
        :param end: Alternative to length; if given, length = end - offset
        """
        self.offset = offset
        if length is None and end is not None:
            length = end - offset + 1
        self.length = length

    def from_bytes(self, data: bytes, offset: int = 0) -> int:
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.
    
        Default no-op implementation.
        Subclasses should override this to parse bytes.

        :param data: The full byte buffer
        :param offset: The current offset from which we start reading
        :return: The new offset after reading
        """
        return offset

    def __repr__(self):
        return f"{self.__class__.__name__}(offset={self.offset}, length={self.length})"


class ValueNode(BaseNode):
    """
    AI BULLSHIT WARNING!
    The below comment was hallucinated by a brainless machine, do NOT trust it.
    Please remove this Warning upon review / verification of correctness.
    
    A node that wraps a single typed value, e.g. uint8, uint16, uint32, cstring, etc.
    """

    def __init__(
        self, name, dtype="uint8", value=None, offset=0, length=None, end=None
    ):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.
    
        :param name: A logical name for this node
        :param dtype: The data type, e.g. 'uint8', 'uint16', 'uint32', 'cstring'
        :param value: Optional initial value or default
        :param offset: Starting offset (in bytes)
        :param length: Number of bytes (if known)
        :param end: Alternative to length; if given, length = end - offset
        """
        super().__init__(offset, length, end)
        self.name = name
        self.dtype = dtype
        self.value = value

    def from_bytes(self, data: bytes, offset=0) -> int:
        match self.dtype:
            case "char":
                # 1 byte
                self.value = struct.unpack_from("<b", data, offset)[0]
                offset += 1

            case "short":
                # 2 bytes, little-endian
                self.value = struct.unpack_from("<h", data, offset)[0]
                offset += 2

            case "long":
                # 4 bytes, little-endian
                self.value = struct.unpack_from("<i", data, offset)[0]
                offset += 4

            case "uchar":
                # 1 byte
                self.value = struct.unpack_from("<B", data, offset)[0]
                offset += 1

            case "ushort":
                # 2 bytes, little-endian
                self.value = struct.unpack_from("<H", data, offset)[0]
                offset += 2

            case "ulong":
                # 4 bytes, little-endian
                self.value = struct.unpack_from("<I", data, offset)[0]
                offset += 4
            case _:
                raise ValueError(f"Unknown dtype: {self.dtype}")

        return offset

    def __repr__(self):
        return (
            f"ValueNode(name={self.name}, dtype={self.dtype}, "
            f"value={self.value}, offset={self.offset}, length={self.length})"
        )


class ValueArray(BaseNode):
    def __init__(self, name, dtype="uint8", values=[], offset=0, length=None, end=None):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.
    
        :param name: A logical name for this node
        :param dtype: The data type, e.g. 'uint8', 'uint16', 'uint32', 'cstring'
        :param value: Optional initial value or default
        :param offset: Starting offset (in bytes)
        :param length: Number of bytes (if known)
        :param end: Alternative to length; if given, length = end - offset
        """
        super().__init__(offset, length, end)
        self.name = name
        self.dtype = dtype
        self.values = values

    def from_bytes(self, data: bytes, offset=0) -> int:
        self.values = []
        starting_offset = offset
        while offset - starting_offset < self.length:
            match self.dtype:
                case "char":
                    # 1 byte
                    self.values.append(struct.unpack_from("<b", data, offset)[0])
                    offset += 1

                case "short":
                    # 2 bytes, little-endian
                    self.values.append(struct.unpack_from("<h", data, offset)[0])
                    offset += 2

                case "long":
                    # 4 bytes, little-endian
                    self.values.append(struct.unpack_from("<i", data, offset)[0])
                    offset += 4

                case "uchar":
                    # 1 byte
                    self.values.append(struct.unpack_from("<B", data, offset)[0])
                    offset += 1

                case "ushort":
                    # 2 bytes, little-endian
                    self.values.append(struct.unpack_from("<H", data, offset)[0])
                    offset += 2

                case "ulong":
                    # 4 bytes, little-endian
                    self.values.append(struct.unpack_from("<I", data, offset)[0])
                    offset += 4
                case _:
                    raise ValueError(f"Unknown dtype: {self.dtype}")

        return offset

    def __repr__(self):
        return (
            f"ValueNode(name={self.name}, dtype={self.dtype}, "
            f"values={self.values}, offset={self.offset}, length={self.length})"
        )


class StructNode(BaseNode):
    """
    AI BULLSHIT WARNING!
    The below comment was hallucinated by a brainless machine, do NOT trust it.
    Please remove this Warning upon review / verification of correctness.
    
    A node that holds multiple named children in a structured way.
    """

    def __init__(self, name, offset=0, length=None, end=None, **children):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.
    
        :param name: Logical name of this struct node.
        :param offset: Starting offset
        :param length: Number of bytes
        :param end: Alternative to length; if given, length = end - offset
        :param children: Named child nodes (ValueNode, StructNode, NodeArray, etc.)
        """
        super().__init__(offset, length, end)
        self.name = name
        self.children = children

    def __getattr__(self, attr):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.
    
        Allows dot-access for children.
        If we have a child node "Foo", then self.Foo returns that child node.
        """
        if attr in self.children:
            return self.children[attr]
        raise AttributeError(
            f"{self.__class__.__name__} '{self.name}' has no child '{attr}'"
        )

    def from_bytes(self, data: bytes, offset: int = 0) -> int:
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.
    
        Calls from_bytes on each child in order, updating the offset.
        Returns the final offset after all children are parsed.

        In production code, you might want to ensure that each child
        stays within this struct’s [self.offset, self.offset + self.length]
        region, if self.length is not None.
        """
        for _, child_node in self.children.items():
            offset = child_node.from_bytes(data, offset)
        return offset

    def __repr__(self):
        child_names = list(self.children.keys())
        return (
            f"StructNode(name={self.name}, offset={self.offset}, "
            f"length={self.length}, children={child_names})"
        )


class NodeArray(BaseNode):
    """
    AI BULLSHIT WARNING!
    The below comment was hallucinated by a brainless machine, do NOT trust it.
    Please remove this Warning upon review / verification of correctness.
    
    A node type that holds a list of sub-nodes in an array.
    """

    def __init__(self, name, nodes=None, offset=0, length=None, end=None):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.
    
        :param name: Logical name of this array
        :param nodes: A list of Node objects
        :param offset: Starting offset
        :param length: Number of bytes
        :param end: Alternative to length; if given, length = end - offset
        """
        super().__init__(offset, length, end)
        self.name = name
        self.nodes = nodes if nodes is not None else []

    def __getitem__(self, index):
        return self.nodes[index]

    def __len__(self):
        return len(self.nodes)

    def from_bytes(self, data: bytes, offset: int = 0) -> int:
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.
    
        Calls from_bytes on each node in the list, updating the offset each time.
        Returns the final offset after parsing all.

        As before, you could enforce that each child must fit within
        [self.offset, self.offset + self.length] if desired.
        """
        for node in self.nodes:
            offset = node.from_bytes(data, offset)
        return offset

    def __repr__(self):
        return (
            f"NodeArray(name={self.name}, offset={self.offset}, "
            f"length={self.length}, nodes={self.nodes})"
        )

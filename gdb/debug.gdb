set disassembly-flavor intel
set pagination off
layout asm
layout regs
focus cmd
disassemble *main
break *main
  

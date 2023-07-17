// test shell code
// gcc -m32 -g -fno-stack-protector -z execstack testshc.c -o testshc -w
#include <sys/mman.h>
#include <errno.h>

const char shellcode[] = "";

void main() {
  char *buf;
  int prot = PROT_READ | PROT_WRITE | PROT_EXEC;
  int flags = MAP_PRIVATE | MAP_ANONYMOUS;

  buf = mmap(0, sizeof(shellcode), prot, flags, -1, 0);
  memcpy(buf, shellcode, sizeof(shellcode));

  ((void (*)(void))buf)();
}

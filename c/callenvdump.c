// gcc -o callenvdump callenvdump.c
/*
  took inspiration from:
    https://stackoverflow.com/a/47160224
    https://stackoverflow.com/a/2085385
    https://stackoverflow.com/a/12059006
    
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/auxv.h>

extern char **environ;

int main(int argc, char *argv[]) {
  char *ptr;
  int i;
  const char delim[] = "=";

  puts("Arguments:");
  for (i = 0; i < argc; i++) {
    printf("  argv[%d]: %p, %p, %s\n", i, argv + i, argv[i], argv[i]);
  }

  puts("\nAuxiliary Vector:");
  // https://man7.org/linux/man-pages/man3/getauxval.3.html
  char * program = (char *)getauxval(AT_EXECFN);
  printf("AT_EXECFN:       %p, %s\n", program, program);

  puts("\nEnvironment:");
  printf("  pointer: %p\n", environ);
  char* underscore = getenv("_");
  printf("  _:       %p, %s\n", underscore, underscore);

  puts("variables:");
  for (char **env = environ; *env != 0; env++)
  {
    char *variable = *env;
    printf("  %s:       %p\n", strtok(variable, delim) ,variable);    
  }

  puts("arguments:");
  for (i = 1; i < argc; i++) {
    ptr = getenv(argv[i]);
    printf("  %s:       %p, %s\n", argv[i], ptr, ptr);
  }

  return 0;
}

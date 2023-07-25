// gcc -o callenvdump callenvdump.c
/*
  took inspiration from:
    https://stackoverflow.com/a/47160224
    https://stackoverflow.com/a/2085385
    https://stackoverflow.com/a/12059006
    https://stackoverflow.com/a/45840521
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/auxv.h>

extern char **environ;

int main(int argc, char *argv[]) {
  char *ptr;
  int i;
  const char delim[2] = "="; // =\0
  const uint ldelim = 1;
  int delimat;

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
  char **env = environ;
  for (; *env; env++)
  {
    char *variable = *env;
    delimat = (int) strcspn(variable, delim);
    printf("  %.*s:       %p\n", delimat, variable, variable + delimat + ldelim);
  }

  puts("arguments:");
  for (i = 1; i < argc; i++) {
    ptr = getenv(argv[i]);
    printf("  %s:       %p, %s\n", argv[i], ptr, ptr);
  }

  return 0;
}

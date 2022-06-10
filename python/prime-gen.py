"""
  Print prime numbers
"""

def isPrime(n):
  for i in range(2, 1+int(n**.5)):
    if not n%i:
      return False
  return True

"""
  FOR CLI ONLY
  
  You can leave this code at the bottom of your package
  and edit main() and mainargs() accordingly
  they will be called if the script is executed via cli
  
  main() can be either called with **mainargs() or providing
  directly all the parameters.
  mainargs() will parse *args as cli arguments and override them
  with **kwargs if needed.
  
  Template by @github.com/ffdevv/code-fu
"""
class Defaults:
  OUTPUT_FILEPATH = None
  FROM = 0
  BITS = 16
  
def main(
    fromNumber: int,
    numberBits: int,
    outputFilePath: str
  ) -> int:
  
  maxNumber = 2**numberBits
  
  if outputFilePath in [None, '']:
    while fromNumber < maxNumber:
      if isPrime(fromNumber):
        print(fromNumber)
      fromNumber += 1
  else:
    with open(outputFilePath, 'a') as fo:
      while fromNumber < maxNumber:
        if isPrime(fromNumber):
          fo.write(str(fromNumber) + "\n")
        fromNumber += 1
  
  return 0

def mainargs(*args, **kwargs):
  from argparse import ArgumentParser
  parser = ArgumentParser(description="Insert Module CLI description")
  parser.add_argument(
    "--from",
    default=Defaults.FROM,
    dest="fromNumber",
    type=int,
    help=f"start from number, default: {Defaults.FROM}",
  )
  parser.add_argument(
    "--bits",
    default=Defaults.BITS,
    dest="bits",
    type=int,
    help=f"stop at highest number with bits, default: {Defaults.BITS}",
  )
  parser.add_argument(
    "-o",
    "--output",
    default=Defaults.OUTPUT_FILEPATH,
    dest="output",
    help=f"output file path, default: stdout",
  )
  _args = parser.parse_args(args)
  return {
    "fromNumber": kwargs.get('fromNumber', _args.fromNumber),
    "numberBits": kwargs.get('numberBits', _args.bits),
    "outputFilePath": kwargs.get('outputFilePath', _args.output)
  }

if __name__ == "__main__":
  import sys
  sys.exit(main(**mainargs(*sys.argv[1:])))

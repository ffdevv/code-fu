"""
  Change Encodings
"""

def reEncode(data: bytes, fromEncoding: str, toEncoding: str) -> bytes:
  return data.decode(fromEncoding).encode(toEncoding)

"""
  FOR CLI ONLY
  
  You can leave this code at the bottom of your package
  and edit main() and mainargs() accordingly
  they will be called if the script is executed via cli
  
  main() can be either called with **mainargs() or providing
  directly all the parameters.
  mainargs() will parse *args as cli arguments and override them
  with **kwargs if needed.
  
  Template by @github.com/ffdevv/pythonfu
"""
import sys

class Defaults:
  INPUT_ENCODING = "utf8"
  OUTPUT_ENCODING = "utf8"
  
def main(
    inputFilePath: str,
    outputFilePath: str,
    inputEncoding: str,
    outputEncoding: str
  ) -> int:
  
  with open(inputFilePath, 'rb') as fi:
    with open(outputFilePath, 'wb') as fo:
      fo.write(reEncode(fi.read(), inputEncoding, outputEncoding))
  
  return 0

def mainargs(*args, **kwargs):
  from argparse import ArgumentParser
  parser = ArgumentParser(description="Insert Module CLI description")
  parser.add_argument(
    dest="inputFilePath",
    help=f"input file",
  )
  parser.add_argument(
    dest="outputFilePath",
    help=f"output file",
  )
  parser.add_argument(
    "--input-encoding",
    default=Defaults.INPUT_ENCODING,
    dest="inputEncoding",
    help=f"input encoding, default: {Defaults.INPUT_ENCODING}",
  )
  parser.add_argument(
    "--output-encoding",
    default=Defaults.OUTPUT_ENCODING,
    dest="outputEncoding",
    help=f"output encoding, default: {Defaults.OUTPUT_ENCODING}",
  )
  _args = parser.parse_args(args)
  return {
    "outputFilePath": kwargs.get('outputFilePath', _args.outputFilePath),
    "inputFilePath": kwargs.get('inputFilePath', _args.inputFilePath),
    "outputEncoding": kwargs.get('outputEncoding', _args.outputEncoding),
    "inputEncoding": kwargs.get('inputEncoding', _args.inputEncoding)
  }

if __name__ == "__main__":
  sys.exit(main(**mainargs(*sys.argv[1:])))

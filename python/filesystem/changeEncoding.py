"""
    Change Encodings via CLI
    Copyright (C) 2022 Federico Fogo

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see https://www.gnu.org/licenses/lgpl-3.0.html
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
  
  Template by @github.com/ffdevv/code-fu
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
  parser = ArgumentParser(description="Change the encoding of a file on a copy")
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

"""
  View Bytes
"""
from typing import Callable

def reprBytes(
    data: bytes, 
    byteRepr: Callable, 
    bytesPerLine: int = 32,
    leftIndent: str = 8*" ",
    quadBytesIndent: str = 4*" ",
    interIndent: str = 1*" ",
    newLine: str = '\n'
  ) -> str:
  l = []
  row = ""
  i = 0
  for byte in data:
    i+=1
    br = byteRepr(byte)
    row += br
    if i % bytesPerLine == 0:
      l.append(row)
      row = ""
    elif i % 4 == 0: 
      row += quadBytesIndent
    else:
      row += interIndent
  if len(row) > 0: l.append(row)
  l = [f"{leftIndent}{r}" for r in l]
  return newLine.join(l)

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
  class Meta:
    SOURCE_STDIN = ""
    BYTES_AS_B16 = lambda b: "%02X" % int.from_bytes(b, 'big')
    BYTES_AS_B10 = lambda b: "%03i" % int.from_bytes(b, 'big')
    INT_AS_B10 = lambda i: "%03i" % i
    INT_AS_B16 = lambda i: "%02X" % i
    FULL_LENGTH = 0

  INPUT_SOURCE = Meta.SOURCE_STDIN
  LENGTH = Meta.FULL_LENGTH

def main(
    inputSource: str,
    byteRepr: Callable,
    length: int
  ) -> int:
  
  if length == Defaults.Meta.FULL_LENGTH: length = None

  if inputSource == Defaults.Meta.SOURCE_STDIN:
    data = sys.stdin.buffer.read(length)
  else:
    with open(inputSource, 'rb') as fi:
      data = fi.read(length)
  
  print(f"Number of bytes: {len(data)}")
  print(f"Hexdump:")
  print(
    reprBytes(data, byteRepr)
  )

  return 0

def mainargs(*args, **kwargs):
  from argparse import ArgumentParser
  parser = ArgumentParser(description="View Bytes")
  parser.add_argument(
    "-f",
    "--input-file",
    default=Defaults.INPUT_SOURCE,
    dest="inputSource",
    help=f"input source file (stdin if '{Defaults.Meta.SOURCE_STDIN}'), default: {Defaults.INPUT_SOURCE}",
  )
  parser.add_argument(
    "-l",
    "--length",
    default=Defaults.LENGTH,
    type=int,
    dest="length",
    help=f"number of bytes to read (all if '{Defaults.Meta.FULL_LENGTH}'), default: {Defaults.LENGTH}",
  )
  parser.add_argument(
    '--base-10', 
    dest='byteRepr', 
    action='store_const',
    const=Defaults.Meta.INT_AS_B10, default=Defaults.Meta.INT_AS_B16,
    help='show bytes as base10 integers (default: base16 integers)',
  )
  _args = parser.parse_args(args)
  return {
    "length": kwargs.get('length', _args.length),
    "inputSource": kwargs.get('inputSource', _args.inputSource),
    "byteRepr": kwargs.get('byteRepr', _args.byteRepr),
  }

if __name__ == "__main__":
  sys.exit(main(**mainargs(*sys.argv[1:])))

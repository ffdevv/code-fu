"""
  Process JSON with custom function
"""
from typing import Union, List
Jsonlike = Union[dict, list]
IntOrString = Union[int, str]

def parseFrom(from_: IntOrString, data: list) -> int:
  if isinstance(from_, int) or from_.isdigit(): return int(from_)
  if from_ == Defaults.Meta.LAST: return len(data)
  if from_ == Defaults.Meta.HALF: return int(len(data) / 2) + 1
  if from_ == Defaults.Meta.FIRST: return 0
  raise ValueError(f"Invalid from: {from_}")

def parseTo(to_: IntOrString, data: list) -> int:
  if isinstance(to_, int) or to_.isdigit(): return int(to_)
  if to_ == Defaults.Meta.LAST: return len(data)
  if to_ == Defaults.Meta.HALF: return int(len(data) / 2) + 1
  if to_ == Defaults.Meta.FIRST: return 0
  raise ValueError(f"Invalid to: {to_}")
  

def processData(data: List[Jsonlike], from_ : IntOrString, to_: IntOrString) -> List[Jsonlike]:
  if len(data) == 0: return data
  from_ = parseFrom(from_, data)
  to_ = parseTo(to_, data)
  return data[from_:to_]
  

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
  class Meta:
    LAST = "last"
    HALF = "half"
    FIRST = "first"
  INPUT_FILEPATH = "./toProcess.json"
  OUTPUT_FILEPATH = "./_processed.json"
  DATA_ENCODING = "utf8"
  FROM = Meta.FIRST
  TO = Meta.LAST
  
def main(
    inputFilePath: str,
    outputFilePath: str,
    dataEncoding: str,
    from_: IntOrString,
    to_: IntOrString
  ) -> int:
  
  import json
  with open(inputFilePath, 'r', encoding=dataEncoding) as fi:
    with open(outputFilePath, 'w') as fo:
      data = processData(json.load(fi), from_ = from_, to_ = to_)
      json.dump(data, fo)

  return 0

def mainargs(*args, **kwargs):
  from argparse import ArgumentParser
  parser = ArgumentParser(description="Process a json file")
  parser.add_argument(
    "-f",
    "--from",
    default=Defaults.FROM,
    dest="from_",
    help=f"from index, default: {Defaults.FROM}",
  )
  parser.add_argument(
    "-t",
    "--to",
    default=Defaults.TO,
    dest="to_",
    help=f"to index, default: {Defaults.TO}",
  )
  parser.add_argument(
    "-i",
    "--input",
    default=Defaults.INPUT_FILEPATH,
    dest="input",
    help=f"input file path, default: {Defaults.INPUT_FILEPATH}",
  )
  parser.add_argument(
    "-o",
    "--output",
    default=Defaults.OUTPUT_FILEPATH,
    dest="output",
    help=f"output file path, default: {Defaults.OUTPUT_FILEPATH}",
  )
  parser.add_argument(
    "--encoding",
    default=Defaults.DATA_ENCODING,
    dest="dataEncoding",
    help=f"output file path, default: {Defaults.DATA_ENCODING}",
  )
  _args = parser.parse_args(args)
  return {
    "inputFilePath": kwargs.get('inputFilePath', _args.input),
    "outputFilePath": kwargs.get('outputFilePath', _args.output),
    "dataEncoding": kwargs.get('dataEncoding', _args.dataEncoding),
    "from_": kwargs.get('from_', _args.from_),
    "to_": kwargs.get('to_', _args.to_)
  }

if __name__ == "__main__":
  import sys
  sys.exit(main(**mainargs(*sys.argv[1:])))

"""
  Process JSON with custom function
"""
from typing import Union
Jsonlike = Union[dict, list]

def processData(data: Jsonlike) -> None:
  
  # code here and modify data
  
  pass
  

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
class Defaults:
  INPUT_FILEPATH = "./toProcess.json"
  OUTPUT_FILEPATH = "./_processed.json"
  DATA_ENCODING = "utf8"
  
def main(
    inputFilePath: str,
    outputFilePath: str,
    dataEncoding: str
  ) -> int:
  
  import json
  with open(inputFilePath, 'r', encoding=dataEncoding) as fi:
    with open(outputFilePath, 'w') as fo:
      data = json.load(fi)
      processData(data)
      json.dump(data, fo)

  return 0

def mainargs(*args, **kwargs):
  from argparse import ArgumentParser
  parser = ArgumentParser(description="Insert Module CLI description")
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
    "dataEncoding": kwargs.get('dataEncoding', _args.dataEncoding)
  }

if __name__ == "__main__":
  import sys
  sys.exit(main(**mainargs(*sys.argv[1:])))

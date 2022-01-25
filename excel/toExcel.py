"""
  Conversions to Excel
"""
import openpyxl
from typing import List

def listOfListsToExcel(
    data: List[list], 
    fpath: str
  ) -> None:
  
  book = openpyxl.Workbook()
  sheet = book.active
  
  for ri in range(1, len(data) + 1):
    for ci in range(1, len(data[ri-1]) + 1):
      sheet.cell(row=ri, column=ci).value = data[ri-1][ci-1]

  book.save(fpath)


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
    JSON_LIST_OF_LISTS = "json[[]]"
    INPUT_TYPES = [
      JSON_LIST_OF_LISTS,
    ]
    
  OUTPUT_FILEPATH = "./toExcel_Output.xlsx"
  DATA_ENCODING = "utf8"
  INPUT_TYPE = Meta.JSON_LIST_OF_LISTS
  INPUT_SOURCE = Meta.SOURCE_STDIN
  
def main(
    inputSource: str,
    inputType: str,
    dataEncoding: str,
    outputFilePath: str
  ) -> int:
  
  # getting data
  if inputSource == Defaults.Meta.SOURCE_STDIN:
    data = sys.stdin.buffer.read()
  else:
    with open(inputSource, 'rb') as fi:
      data = fi.read()
  data = data.decode(dataEncoding)
  
  # processing data
  # [[]]
  if inputType == Defaults.Meta.JSON_LIST_OF_LISTS:
    from json import loads
    listOfListsToExcel(loads(data), outputFilePath)
  
  return 0

def mainargs(*args, **kwargs):
  from argparse import ArgumentParser
  parser = ArgumentParser(description="Quickly build excel tables from different sources")
  parser.add_argument(
    "-f",
    "--input-file",
    default=Defaults.INPUT_SOURCE,
    dest="inputSource",
    help=f"input source file (stdin if '{Defaults.Meta.SOURCE_STDIN}'), default: {Defaults.INPUT_SOURCE}",
  )
  parser.add_argument(
    "-t",
    "--input-type",
    default=Defaults.INPUT_TYPE,
    dest="inputType",
    help=f"input type (values: {', '.join(Defaults.Meta.INPUT_TYPES)}). Default: {Defaults.INPUT_TYPE}",
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
    "inputSource": kwargs.get('inputSource', _args.inputSource),
    "inputType": kwargs.get('inputType', _args.inputType),
    "outputFilePath": kwargs.get('outputFilePath', _args.output),
    "dataEncoding": kwargs.get('dataEncoding', _args.dataEncoding)
  }

if __name__ == "__main__":
  sys.exit(main(**mainargs(*sys.argv[1:])))

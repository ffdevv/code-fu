"""
  Utility for incrementals salarial classes

  eg:
    from salaries import *
    classe = parseClass("66'454 68'821 71'188 73'556 75'923 77'817 79'711 81'605 83'499 85'393 86'971 88'549 90'128 91'706 93'284 94'863 95'915 96'967 98'019 99'071 100'124 101'176 102'228 103'280 104'332")
    scattiAssoluti = absIncrements(classe)
    scattiPercentuali = pcIncrements(classe)
    all80percento = castInt(atPercentage(.8, classe))
    mensile80 = monthly(all80percento)
    spese = fixedOutflow(1500, 500, 250, 400, 150, nItems = classe)
    tasse = atPercentage(.22, mensile80)
    uscite = sumLists(spese, tasse)
    netto = castInt(netOf(uscite, mensile80))
"""
from typing import List, Union

ListOfNumbers = List[Union[int, float]]
ListOfInt = List[int]

def castInt(ln : ListOfNumbers) -> ListOfInt:
  return [int(x) for x in ln]

def parseClass(text: str) -> ListOfInt:
  """
  Returns a list of items of type int
  """
  newline_separated = text.replace("'", "").replace(" ","\n").replace(",","\n")
  return [int(s) for s in filter(lambda x: bool(x), newline_separated.split("\n"))]

def absIncrements(sc : ListOfNumbers) -> ListOfNumbers:
  """
  Returns a list representing each year bonus in absolute value
  """
  return [sc[i] - sc[i-1] for i in range(1, len(sc))]

def pcIncrements(sc : ListOfNumbers) -> ListOfNumbers:
  """
  Returns a list representing each year bonus in percentage against the previous year
  """
  return [((sc[i] / sc[i-1]) - 1) for i in range(1, len(sc))]

def atPercentage(pc : float, ln : ListOfNumbers) -> ListOfNumbers:
  """
  Returns the computed percentage for each member of the list
  """
  return [pc * x for x in ln]

def monthly(sc : ListOfNumbers, months = 13) -> ListOfInt:
  """
  Compute the monthly salary of each item of the salarial class
  """
  return [x // months for x in sc]

def yearly(msc : ListOfNumbers, months = 13) -> ListOfNumbers:
  """
  Compute the yearly salary of each item of the monthly salarial class
  """
  return [x * months for x in msc]

def netOf(outflowList, baseList):
  """
  Subtract from the baseList the respective item of the outflowList
  """
  return [x - y for x, y in zip(baseList, outflowList)]

def fixedOutflow(
    *voices : ListOfNumbers, 
    nItems : Union[int,list] = 25
  ) -> ListOfNumbers:
  """
  Sum voices and build a list made of nItems items
  """
  return [sum(voices) for _ in range(nItems if isinstance(nItems, int) else len(nItems))]

def sumLists(*lists : List[ListOfNumbers]):
  return [sum(x) for x in zip(*lists)]

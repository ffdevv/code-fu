"""
  Utilities for working with arrays
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

from functools import reduce
from typing import Callable

def get(a: list, i: int, fallback = None):
  """
  Like dict.get
  """
  return a[i] if -1 < i < len(a) else fallback

def nestedGet(a: list, k: str, sep: str = "."):
  """
  Like get but works with <sep> nested patterns
  """
  return reduce(lambda acc, itm: get(acc, int(itm)) if isinstance(acc, list) else None, k.split(sep), a)
  
def popIf(a: list, i: int, f: Callable = lambda v: True):
  """
  Pop the item at index <i> from <a> if <f>(value) returns True
  Does not throw in case <i> not in <a>
  """
  return a.pop(i) if -1 < i < len(a) and f(a[i]) else None

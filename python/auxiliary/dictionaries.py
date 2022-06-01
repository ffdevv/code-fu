"""
  Utilities for working with dictionaries
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

def nestedGet(d: dict, k: str, sep: str = "."):
  """
  Like dict.get() but works with <sep> nested patterns
  """
  return reduce(lambda acc, itm: acc.get(itm) if isinstance(acc, dict) else None, k.split(sep), d)

def popIf(d: dict, k: str, f: Callable = lambda v: True):
  """
  Pop the key from the dict if <f>(value) returns True
  Does not throw in case <k> not in <d>
  """
  return d.pop(k) if k in d.keys() and f(d[k]) else None

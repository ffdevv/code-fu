"""
  Mono-file with very usefull classes to build utility functions quickly for any project
  It follows the logic of https://cyberchef.org/ and implements that logic into python classes

  ---
  After inserting your local copy of this file you can reference it and wrap up recipes.
  
  ---
  EG 1 Make a data process readable
    from .auxiliary.cyber_chef import Recipe
    
    serialize_object = Recipe(
      lambda o: o.__dict__,    # take the dict of the object
      "json_to_str",           # make a json string of it
      ("str_to_bytes", "utf8") # encode the string into bytes
      "bytes_to_b64"           # make a base64 string of those
    ).wrap()                   # or .wrap_debug(print) if you wanna dbg
    
    unserialize_object = Recipe(
      "b64_to_bytes",
      ("bytes_to_str", "utf8"),
      "str_to_json",
      o.from_object
    ).wrap()
  
  ----
  
  
  EG 2 don't waste time rebuilding the wheel every time
    from .auxiliary.cyber_chef import Recipes
    
    urlencode = Recipes.get('urlencoded').wrap()
    encode_data_for_http_request = Recipes.get('to_urlencoded_b64_string').wrap()
    ...
    
"""

from urllib.parse import quote as urlencode, unquote as urldecode
from json import dumps as json_dumps, loads as json_loads
from base64 import b64encode, b64decode
from typing import Callable, Optional

def cast_to_str(v, encoding = 'utf8'):
  if isinstance(v, str):
    return v
  if isinstance(v, (int, float)):
    return str(v)
  if isinstance(v, bool):
    return "true" if v else "false"
  if isinstance(v, bytes):
    return v.decode(encoding)
  raise ValueError(f"Cannot cast type {v.__class__.__name__} into string")
  
def cast_to_bytes(v, encoding = 'utf8') -> bytes:
  if isinstance(v, str):
    return v.encode(encoding)
  if isinstance(v, (int, float)):
    return str(v).encode(encoding)
  if isinstance(v, bool):
    return "true".encode(encoding) if v else "false".encode(encoding)
  if isinstance(v, bytes):
    return v
  raise ValueError(f"Cannot cast type {v.__class__.__name__} into bytes")

def hex_to_bytes(h: str) -> bytes:
  return bytes.fromhex(h)

def bytes_to_hex(
    b: bytes, 
    sep: Optional[str] = None, 
    bytes_per_block: Optional[int] = None,
    upper: bool = False
  ) -> str:
  if sep is None:
    ret = b.hex()
  else:
    ret = b.hex(
      sep,
      # negative values separe from left to right
      bytes_per_block * -1 if bytes_per_block else 0
    )
  return ret.upper() if upper else ret

def str_to_bytes(s: str, encoding = 'utf8') -> bytes:
  return s.encode(encoding)

def bytes_to_str(b: bytes, encoding = 'utf8') -> str:
  return b.decode(encoding)

def int_to_octet(i: int) -> str:
  if any((i > 255, i < 0)):
    raise ValueError("Octet can represent 0-255 int values only")
  return f"{i:08b}"

def octet_to_int(o: str) -> int:
  if any((len(o) != 8, (o.count('0') + o.count('1') != 8))):
    raise TypeError("Invalid octet")
  ret = 0
  for i, bit in o:
    if bit == '1':
      ret += 2 ** i
  return ret

def bytes_to_ints(b: bytes) -> [int]:
  return [int(b_) for b_ in b]

def ints_to_bytes(ints: [int]) -> bytes:
  return b''.join([i.to_bytes(1, 'big') for i in ints])
  
class Ingredient:
  def __init__(self, name, func, *args, **kwargs):
    self.name = name
    self.func = func
    self.args = args
    self.kwargs = kwargs
    
  def wrap(self):
    def wrapped(value):
      return self.func(value, *self.args, **self.kwargs)
    return wrapped

  @property
  def args(self):
    """Positional arguments."""
    return self._args
  
  @args.setter 
  def args(self, value):
    if value is None:
      self._args = []
      return
    if not isinstance(value, (list, tuple)):
      self._args = [value]
      return
    self._args = list(value)

  @property
  def kwargs(self):
    """Keyword arguments."""
    return self._kwargs

  @kwargs.setter    
  def kwargs(self, value):
    if value is None:
      self._kwargs = {}
      return
    self._kwargs = dict(value)

  def __repr__(self):
    return (
        f"Ingredient<{self.name}" + \
        f" {'*args' if self.args else ''}" + \
        f" {'**kwargs' if self.kwargs else ''}"
    ).strip() + ">"

class Ingredients:
  bytes_to_b64 = Ingredient("bytes_to_b64", b64encode)
  b64_to_bytes = Ingredient("b64_to_bytes", b64decode)
  urlencode    = Ingredient("urlencode", urlencode)
  urldecode    = Ingredient("urldecode", urldecode)
  json_to_str  = Ingredient("json_to_str", json_dumps)
  str_to_json  = Ingredient("str_to_json", json_loads)
  hex_to_bytes = Ingredient("hex_to_bytes", hex_to_bytes)
  bytes_to_hex = Ingredient("bytes_to_hex", bytes_to_hex)
  cast_to_bytes= Ingredient("cast_to_bytes", cast_to_bytes)
  cast_to_str  = Ingredient("cast_to_str", cast_to_str)
  str_to_bytes = Ingredient("str_to_bytes", str_to_bytes)
  bytes_to_str = Ingredient("bytes_to_str", bytes_to_str)
  int_to_octet = Ingredient("int_to_octet", int_to_octet)
  octet_to_int = Ingredient("octet_to_int", octet_to_int)
  bytes_to_ints= Ingredient("bytes_to_ints", bytes_to_ints)
  ints_to_bytes= Ingredient("ints_to_bytes", ints_to_bytes)
  
  @classmethod
  def get(cls, name, default = None, raise_on_None = True):
    i = getattr(cls, name, default)
    if raise_on_None and (i is None):
      raise ValueError(f"Ingredient {name} not available")
    return i

class Recipe:
  def __init__(self, *args):
    self.ingredients = []
    for arg in args:
      if isinstance(arg, tuple):
        la=len(arg)
        if la == 3:
          n, a, kw = (
            arg[0], 
            arg[1], 
            arg[2]
          )
        elif la == 2:
          n, a, kw = (
            arg[0], 
            arg[1],
            {}
          )
        elif la == 1:
          n, a, kw = arg, [], {}
        else:
          raise TypeError("argument tuples length not supported")
        arg = Ingredients.get(n, raise_on_None=True)
        arg.args = a
        arg.kwargs = kw
      elif isinstance(arg, str):
        arg = Ingredients.get(arg, raise_on_None=True)
      if not (callable(arg) or isinstance(arg, Ingredient)):
        raise ValueError("pass functions or ingredients names")
      self.ingredients.append(arg)

  def wrap(self):
    def wrapped(value):
      for ingredient in self.ingredients:
        if isinstance(ingredient, Ingredient):
          value = ingredient.wrap()(value)
        else:
          value = ingredient(value)
      return value
    return wrapped

  def wrap_debug(self, dbg: Callable):
    def wrapped(value):
      for step, ingredient in enumerate(self.ingredients):
        if isinstance(ingredient, Ingredient):
          value = ingredient.wrap()(value)
        else:
          value = ingredient(value)
        dbg(step, ingredient, value)
      return value
    return wrapped

  def cook(self, v, dbg: Optional[Callable] = None):
    return (
      self.wrap()(v) if not callable(dbg) 
      else self.wrap_debug(dbg)(v)
    )

class Recipes:
  urlencoded = Recipe(
    lambda s: str(s) if isinstance(s, (int, float)) else s,  # cast numbers to strings
    "urlencode"                                              # then urlencode
  )

  to_urlencoded_b64_string = Recipe(
    lambda s: coherce_bytes(s, 'utf8'),   # cast everything to bytes
    "bytes_to_b64",                       # get a b64 encoded str
    "urlencode"                           # urlencode it
  )

  @classmethod
  def get(cls, name, default = None, raise_on_None = True):
    i = getattr(cls, name, default)
    if raise_on_None and (i is None):
      raise ValueError(f"Recipe {name} not available")
    return i

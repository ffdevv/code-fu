"""
  Mono-file with very usefull classes to build utility functions quickly for any project
  It follows the logic of https://cyberchef.org/ and implements that logic into python classes

  ---
  After inserting your local copy of this file you can reference it and wrap up recipes.
  
  ---
  EG 1 Make a data process readable
    from .auxiliary.cyber_chef import Recipe
    
    serialize_object = Recipe("serialize_object", # name of the recipe
      lambda o: o.__dict__,    # take the dict of the object
      "json_to_str",           # make a json string of it
      ("str_to_bytes", "utf8") # encode the string into bytes
      "bytes_to_b64"           # make a base64 string of those
    ).wrap()                   # or .wrap_debug(print) if you wanna dbg
    
    unserialize_object = Recipe("unserialize_object", # name of the recipe
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


  ----
  
  
  EG 3 quickly build high level function
    from .auxiliary.cyber_chef import Recipes, Ingredients
    
    def encrypt_string_with_password(s, p):
      # derive a secret_key of 32 bytes 
      # aes256 will use fixed length keys
      # and the password won't be directly used
      secret_key = Ingredients.get('derive_key_pbkdf2_sha512').cook(p)
      
      # customize the recipe
      recipe = Recipes.get('encrypt_string')
      recipe.ingredients[1].kwargs['key'] = secret_key
      
      return recipe.cook(s), secret_key

    def decrypt_string_with_secret_key(e, k):
      recipe = Recipes.get('decrypt_string')
      recipe.ingredients[1].kwargs['key'] = k
      return recipe.cook(e)

    s1 = 'lol'
    encrypted, secret_key = encrypt_string_with_password(s1, 'lel')
    s1 == decrypt_string_with_secret_key(encrypted, secret_key)

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

def hash_keccak(b: bytes, digest_bits: int=256) -> bytes:
  from Crypto.Hash import keccak
  h = keccak.new(digest_bits = digest_bits)
  h.update(b)
  return h.digest()

def hash_sha256(b: bytes) -> bytes:
  from Crypto.Hash import SHA256
  return SHA256.new(b).digest()

def hash_sha512(b: bytes) -> bytes:
  from Crypto.Hash import SHA512
  return SHA512.new(b).digest()

def hash_md5(b: bytes) -> bytes:
  from Crypto.Hash import MD5
  return MD5.new(b).digest()

def sign_hmac_sha256(secret: bytes, data: bytes) -> bytes:
  from Crypto.Hash import HMAC, SHA256
  h = HMAC.new(secret, digestmod=SHA256)
  h.update(data)
  return h.digest()

def derive_key_pbkdf2_sha512(
    secret: bytes, 
    length: int,
    salt_bytes: int = 16,
    iterations: int = 10 ** 6
  ) -> bytes:
  from Crypto.Protocol.KDF import PBKDF2
  from Crypto.Hash import SHA512
  from Crypto.Random import get_random_bytes

  salt = get_random_bytes(salt_bytes)
  b = PBKDF2(secret, salt, length, count=iterations, hmac_hash_module=SHA512)
  return b

def password_hash_bcrypt(
    password: bytes, 
    iterations: int = 12, 
    sha256_b64_preprocess: bool = False
  ) -> bytes:
  from Crypto.Protocol.KDF import bcrypt
  from Crypto.Hash import SHA256

  if sha256_b64_preprocess:
    # necessary to bcrypt passwords longer than 72 bytes
    password = b64encode(SHA256.new(password).digest())
  
  return bcrypt(password, iterations)

def password_check_bcrypt(
    plaintext_password: bytes, 
    hashed_password: bytes,
    sha256_b64_preprocess: bool = False
  ) -> bool:
  from Crypto.Protocol.KDF import bcrypt
  from Crypto.Hash import SHA256

  if sha256_b64_preprocess:
    # necessary to bcrypt passwords longer than 72 bytes
    plaintext_password = b64encode(
      SHA256.new(plaintext_password).digest()
    )
  
  try:
    return bcrypt_check(
      plaintext_password, 
      hashed_password
    )
  except ValueError:
    return False

def encrypt_aes256_gcm(
    data: bytes,
    key: bytes,
    header: bytes = b'',
    nonce: Optional[bytes] = None,
    mac_tag_length: int = 16
  ) -> dict:
  from Crypto.Cipher import AES
  from Crypto.Random import get_random_bytes

  if not len(key) in [16, 24, 32]:
    raise ValueError("AES256 GCM work only keys of (16, 24 or 32) bytes")

  if nonce is not None and len(nonce) < 12:
    raise ValueError("AES256 GCM nonce must be at least 12 bytes long")

  if mac_tag_length < 4 or mac_tag_length > 16:
    raise ValueError("AES256 GCM mac tag length must be between 4 and 16 bytes long")

  cipher = AES.new(
    key, 
    AES.MODE_GCM, 
    nonce=nonce, 
    mac_len=mac_tag_length
  )
  cipher.update(header)
  ciphertext, tag = cipher.encrypt_and_digest(data)
  d_keys = ['nonce', 'header', 'ciphertext', 'tag']
  d_values = [
    b64encode(x).decode('utf-8') 
    for x in (cipher.nonce, header, ciphertext, tag)
  ]
  return dict(zip(d_keys, d_values))

def decrypt_aes256_gcm(
    d: dict,
    key: bytes,
  ) -> bytes:
  from base64 import b64decode
  from Crypto.Cipher import AES
  from Crypto.Util.Padding import unpad
  
  try:
    d_keys = [ 'nonce', 'header', 'ciphertext', 'tag' ]
    d_bytes = {k:b64decode(d[k]) for k in d_keys}
    cipher = AES.new(key, AES.MODE_GCM, nonce=d_bytes['nonce'])
    cipher.update(d_bytes['header'])
    data = cipher.decrypt_and_verify(d_bytes['ciphertext'], d_bytes['tag'])
    return data
  
  except (ValueError, KeyError) as e:
    raise e

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

  def cook(self, value):
    return self.wrap()(value)

  def clone(self) -> "Ingredient":
    return Ingredient(self.name, self.func, *self.args, **self.kwargs)

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
  to_json      = Ingredient("to_json", json_dumps)
  from_json    = Ingredient("from_json", json_loads)
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
  hash_keccak  = Ingredient("hash_keccak", hash_keccak)
  hash_sha256  = Ingredient("hash_sha256", hash_sha256)
  hash_sha512  = Ingredient("hash_sha512", hash_sha512)
  hash_md5     = Ingredient("hash_md5", hash_md5)
  sign_hmac_sha256 = Ingredient("sign_hmac_sha256", sign_hmac_sha256)
  derive_key_pbkdf2_sha512 = Ingredient("derive_key_pbkdf2_sha512", derive_key_pbkdf2_sha512, 32)
  password_hash_bcrypt  = Ingredient("password_hash_bcrypt", password_hash_bcrypt)
  password_check_bcrypt = Ingredient("password_check_bcrypt", password_check_bcrypt)
  encrypt_aes256_gcm    = Ingredient("encrypt_aes256_gcm", encrypt_aes256_gcm)
  decrypt_aes256_gcm    = Ingredient("decrypt_aes256_gcm", decrypt_aes256_gcm)
  
  _methods = ['get', 'add', 'list', 'grep']

  @classmethod
  def get(cls, name, default = None, raise_on_None = True):
    i = getattr(cls, name, default)
    if raise_on_None and (i is None):
      raise ValueError(f"Ingredient {name} not available")
    return i.clone()
  
  @classmethod
  def add(cls, ingredient):
    setattr(cls, ingredient.name, ingredient)
    return getattr(cls, ingredient.name, None)

  @classmethod
  def list(cls):
    return list(filter(
      lambda k: not any((k.startswith('_'), k in cls._methods)),
      cls.__dict__.keys())
    )

  @classmethod
  def grep(cls, s):
    return list(filter(lambda k: s in k, cls.list()))

class Recipe:
  def __init__(self, name, *args):
    self.name = name
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
        raise ValueError("pass functions or ingredient names")
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

  def clone(self) -> "Recipe":
    return Recipe(self.name, *self.ingredients)

class Recipes:
  urlencoded = Recipe("urlencoded",
    lambda s: str(s) if isinstance(s, (int, float)) else s,  # cast numbers to strings
    "urlencode"                                              # then urlencode
  )

  to_urlencoded_b64_string = Recipe("to_urlencoded_b64_string",
    lambda s: coherce_bytes(s, 'utf8'),   # cast everything to bytes
    "bytes_to_b64",                       # get a b64 encoded str
    "urlencode"                           # urlencode it
  )

  hash_string = Recipe("hash_string",
    "str_to_bytes",
    "hash_sha256",
    "bytes_to_hex"
  )

  encrypt_string = Recipe("encrypt_string",
    "str_to_bytes",
    ("encrypt_aes256_gcm", [], {"key": b'1234' * 4}),
    "to_json"
  )

  decrypt_string = Recipe("decrypt_string",
    "from_json",
    ("decrypt_aes256_gcm", [], {"key": b'1234' * 4}),
    "bytes_to_str"
  )

  _methods = ['get', 'add', 'list', 'grep']

  @classmethod
  def get(cls, name, default = None, raise_on_None = True):
    i = getattr(cls, name, default)
    if raise_on_None and (i is None):
      raise ValueError(f"Recipe {name} not available")
    return i.clone()
    
  @classmethod
  def add(cls, recipe):
    setattr(cls, recipe.name, recipe)
    return getattr(cls, recipe.name, None)

  @classmethod
  def list(cls):
    return list(filter(
      lambda k: not any((k.startswith('_'), k in cls._methods)),
      cls.__dict__.keys())
    )

  @classmethod
  def grep(cls, s):
    return list(filter(lambda k: s in k, cls.list()))

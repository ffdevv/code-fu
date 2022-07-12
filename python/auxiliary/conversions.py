def bytes2bigint(uint8s):
  """
  Convert a list of bytes to a single big integer
  """
  i = 0
  for uint8 in uint8s:
    i *= 256
    i += uint8
  return i

def bigint2bytes(bigint):
  """
  Convert a single big integer to a list of bytes
  """
  bytes_ = b''
  while bigint:
    bytes_ += bytes([bigint % 256])
    bigint //= 256
  return bytes(reversed(bytes_))
  

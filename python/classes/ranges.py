from collections import OrderedDict
from typing import Dict, Union

KwargsType = Dict[str, Union[int, float]] # label: upper boundary

class Ranges():
  """
  Class to hold numeric ranges to quickly get labels using a value as the key in a dict-like approach
  usage:
    skill_levels = Ranges( Beginner = 10, Intermediate = 20, Advanced = 30, Expert = 40, Guru = Ranges.INFINITE )
    print(
      skill_levels[5],
      skill_levels[18],
      skill_levels[23],
      skill_levels[34],
      skill_levels[46],
      skill_levels[12901]
    )      
  """
  INFINITE = float('inf')

  def __init__(self, **kwargs : KwargsType):
    self._d = OrderedDict((v,k) for k,v in sorted(kwargs.items(), key=lambda i: i[1]))

  def __getitem__(self, k):
    _sks = list(self._d.keys())
    _k = k
    for ub in _sks:
      _k = ub
      if k <= ub:
        break
    return self._d.get(_k)

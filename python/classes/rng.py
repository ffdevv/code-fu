import random as _random
from typing import Tuple, Sequence, Optional, Union

Weight = Union[int, float]
RndOutcome = Tuple["T", Weight]

def random() -> float:
    """
    Generate a random float in the range [0, 1)
    
    Example:
    >>> random()
    0.8413271742929447
    
    Returns:
    float: Random float in the range [0, 1)
    """
    return _random.random()

def rndbetween(from_: int, to: int) -> int:
    """
    Generate a random integer between two numbers (inclusive)
    
    Args:
    from_ (int): Lower bound of the range.
    to (int): Upper bound of the range.
    
    Example:
    >>> rndbetween(1, 10)
    6
    
    Returns:
    int: Random integer between from_ and to.
    """
    return _random.randint(from_, to)

def rndindexw(
        seq: Sequence, 
        weights: Sequence[Weight]
    ) -> int:
    """
    Get a random index from a sequence, given an associated sequence of weights.
    
    Args:
    seq (Sequence): The sequence to choose from.
    weights (Sequence[Weight]): A sequence of weights, corresponding to seq.
    
    Example:
    >>> rndindexw(['a', 'b', 'c'], [1, 3, 1])
    1
    
    Returns:
    int: The index of the chosen element in seq.
    """
    return _random.choices(list(range(len(seq))), weights, k=1)[0]

def rndindexesw(
        seq: Sequence, 
        weights: Sequence[Weight], 
        k: int
    ) -> int:
    """
    Get k random indexes from a sequence, given an associated sequence of weights.
    
    Args:
    seq (Sequence): The sequence to choose from.
    weights (Sequence[Weight]): A sequence of weights, corresponding to seq.
    k (int): The number of indexes to choose.
    
    Example:
    >>> rndindexesw(['a', 'b', 'c'], [1, 3, 1], 2)
    [1, 1]
    
    Returns:
    list[int]: The indexes of the chosen elements in seq.
    """
    return _random.choices(list(range(len(seq))), weights, k=k)

def rndindex(seq: Sequence) -> int:
    """
    Get a random index from a sequence.
    
    Args:
    seq (Sequence): The sequence to choose from.
    
    Example:
    >>> rndindex(['a', 'b', 'c'])
    2
    
    Returns:
    int: The index of the chosen element in seq.
    
    Raises:
    IndexError: If seq is empty.
    """
    ls = len(seq)
    if ls == 0:
        raise IndexError("Cannot get a random index from an empty sequence")
    return rndbetween(0, ls - 1)

def rndindexes(seq: Sequence, k: int) -> Sequence[int]:
    """
    Get k random indexes from a sequence.
    
    Args:
    seq (Sequence): The sequence to choose from.
    k (int): The number of indexes to choose.
    
    Example:
    >>> rndindexes(['a', 'b', 'c'], 2)
    [2, 0]
    
    Returns:
    list[int]: The indexes of the chosen elements in seq.
    
    Raises:
    IndexError: If seq is empty.
    """
    ls = len(seq)
    if ls == 0:
        raise IndexError("Cannot get a random index from an empty sequence")
    return [rndbetween(0, ls - 1) for _ in range(k)]
    
def rnditem(seq: Sequence["T"]) -> "T":
    """
    Get a random element from a sequence.
    
    Args:
    seq (Sequence["T"]): The sequence to choose from.
    
    Example:
    >>> rnditem(['a', 'b', 'c'])
    'c'
    
    Returns:
    "T": The chosen element from seq.
    """
    return seq[rndindex(seq)]

def rnditems(seq: Sequence["T"], k: int) -> Sequence["T"]:
    """
    Get k random elements from a sequence.
    
    Args:
    seq (Sequence["T"]): The sequence to choose from.
    k (int): The number of elements to choose.
    
    Example:
    >>> rnditems(['a', 'b', 'c'], 2)
    ['c', 'a']
    
    Returns:
    list["T"]: The chosen elements from seq.
    """
    return [seq[i] for i in rndindexes(seq, k)]

def rnditemw(seq: Sequence["T"], weights: Sequence[Weight]) -> "T":
    """
    Get a random element from a sequence, given an associated sequence of weights.
    
    Args:
    seq (Sequence["T"]): The sequence to choose from.
    weights (Sequence[Weight]): A sequence of weights, corresponding to seq.
    
    Example:
    >>> rnditemw(['a', 'b', 'c'], [1, 3, 1])
    'b'
    
    Returns:
    "T": The chosen element from seq.
    """
    return seq[rndindexw(seq, weights)]

def rnditemsw(seq: Sequence["T"], weights: Sequence[Weight], k: int) -> Sequence["T"]:
    """
    Get k random elements from a sequence, given an associated sequence of weights.
    
    Args:
    seq (Sequence["T"]): The sequence to choose from.
    weights (Sequence[Weight]): A sequence of weights, corresponding to seq.
    k (int): The number of elements to choose.
    
    Example:
    >>> rnditemsw(['a', 'b', 'c'], [1, 3, 1], 2)
    ['b', 'b']
    
    Returns:
    list["T"]: The chosen elements from seq.
    """
    return [seq[i] for i in rndindexesw(seq, weights, k)]

class RndPicker:
    """
    A class for randomly picking outcomes with a certain weight.
    
    Example:
    >>> rp = RndPicker([("outcome1", 1), ("outcome2", 3)])
    >>> rp.pick_one()
    'outcome2'
    
    Args:
    outcomes (Optional[Sequence[RndOutcome]]): A sequence of outcomes and their weights. Defaults to None.
    """
    def __init__(self, outcomes: Optional[Sequence[RndOutcome]] = None):
        self._outcomes = [*(outcomes or [])]
    
    def __getitem__(self, k):
        """
        Get the weight of an outcome.
        
        Args:
        k (any): The outcome to look for.
        
        Returns:
        Weight: The weight of the outcome.
        """
        return self._outcomes[self.results.index(k)][1]

    def __setitem__(self, k, v):
        """
        Set the weight of an outcome.
        
        Args:
        k (any): The outcome to change.
        v (Weight): The new weight of the outcome.
        """
        try:
            ir = self.results.index(k)
        except ValueError:
            self.add_outcome(k, v)
            return
        self._outcomes[ir] = (k, v)
        
    def __len__(self):
        """
        Get the number of outcomes.
        
        Returns:
        int: The number of outcomes.
        """
        return len(self._outcomes)

    def _pick_one_w(self):
        """
        Pick one outcome using the weights.
        
        Returns:
        any: The picked outcome.
        """
        return rnditemw(self.results, self.weights)
    
    def _pick_one_u(self):
        """
        Pick one outcome without using the weights.
        
        Returns:
        any: The picked outcome.
        """
        return rnditem(self.results)
    
    def _pick_many_w(self, k: int):
        """
        Pick k outcomes using the weights.
        
        Args:
        k (int): The number of outcomes to pick.
        
        Returns:
        list[any]: The picked outcomes.
        """
        return rnditemsw(self.results, self.weights, k)
    
    def _pick_many_u(self, k: int):
        """
        Pick k outcomes without using the weights.
        
        Args:
        k (int): The number of outcomes to pick.
        
        Returns:
        list[any]: The picked outcomes.
        """
        return rnditems(self.results, k)

    def keys(self):
        """
        Get the outcomes.
        
        Returns:
        list[any]: The outcomes.
        """
        return self.results
    
    def values(self):
        """
        Get the weights.
        
        Returns:
        list[Weight]: The weights.
        """
        return self.weights
    
    def items(self):
        """
        Get the outcomes and their weights.
        
        Returns:
        generator: A generator of tuples, where each tuple is an outcome and its weight.
        """
        return ((k, v) for k, v in zip(self.results, self.weights))
        
    @property 
    def outcomes(self):
        """
        Get the outcomes and their weights.
        
        Returns:
        list[RndOutcome]: The outcomes and their weights.
        """
        return self._outcomes
    
    @property
    def weights(self):
        """
        Get the weights.
        
        Returns:
        list[Weight]: The weights.
        """
        return list(map(lambda o: o[1], self._outcomes))
    
    @property
    def results(self):
        """
        Get the outcomes.
        
        Returns:
        list[any]: The outcomes.
        """
        return list(map(lambda o: o[0], self._outcomes))
    
    @property
    def total_weight(self) -> Weight:
        """
        Get the total weight.
        
        Returns:
        Weight: The total weight.
        """
        return sum(self.weights)
    
    @property
    def equal_weights(self) -> bool:
        """
        Check if all weights are equal.
        
        Returns:
        bool: True if all weights are equal, False otherwise.
        """
        weights = self.weights
        return all(w == weights[0] for w in weights) if len(weights) else True
    
    def missing_weight(self, aimed_weight: Weight = 100) -> Weight:
        """
        Get the weight that is missing to reach a certain total.
        
        Args:
        aimed_weight (Weight): The aimed total weight. Defaults to 100.
        
        Returns:
        Weight: The missing weight.
        """
        return aimed_weight - self.total_weight
    
    def add_outcome(self, result: "T", weight: Weight = 1) -> "RndPicker":
        """
        Add an outcome.
        
        Args:
        result (any): The outcome to add.
        weight (Weight): The weight of the outcome. Defaults to 1.
        
        Returns:
        RndPicker: The RndPicker instance.
        
        Raises:
        ValueError: If the outcome already exists.
        """
        if result in self.results:
            raise ValueError("Outcome already existing (use set())")
        self._outcomes.append((result, weight))
        return self
    
    def set_outcome(self, result: "T", weight: Weight, upsert: bool = True) -> "RndPicker":
        """
        Set the weight of an outcome. If the outcome doesn't exist, add it.
        
        Args:
        result (any): The outcome to change or add.
        weight (Weight): The new weight of the outcome.
        upsert (bool): If True, add the outcome if it doesn't exist. If False, only change existing outcomes. Defaults to True.
        
        Returns:
        RndPicker: The RndPicker instance.
        
        Raises:
        IndexError: If upsert is False and the outcome doesn't exist.
        """
        if not upsert and result in self.results:
            raise IndexError("Outcome not found")
        self[result] = weight
        return self
    
    def rm_outcome(self, result: "T", raise_: bool = True) -> "RndPicker":
        """
        Remove an outcome.
        
        Args:
        result (any): The outcome to remove.
        raise_ (bool): If True, raise an error if the outcome doesn't exist. If False, do nothing. Defaults to True.
        
        Returns:
        RndPicker: The RndPicker instance.
        
        Raises:
        IndexError: If raise_ is True and the outcome doesn't exist.
        """
        try:
            ir = self.results.index(result)
        except ValueError:
            if raise_:
                raise IndexError("Outcome not found")
            return self
        self._outcomes.pop(ir)
        return self
    
    def pick_one(self, weighted: bool = True):
        """
        Pick one outcome.
        
        Args:
        weighted (bool): If True, use the weights to pick an outcome. If False, ignore the weights. Defaults to True.
        
        Returns:
        any: The picked outcome.
        """
        if weighted:
            return self._pick_one_w()
        return self._pick_one_u()
    
    def pick_many(self, k: int, weighted: bool = True):
        """
        Pick k outcomes.
        
        Args:
        k (int): The number of outcomes to pick.
        weighted (bool): If True, use the weights to pick the outcomes. If False, ignore the weights. Defaults to True.
        
        Returns:
        list[any]: The picked outcomes.
        """
        if weighted:
            return self._pick_many_w(k)
        return self._pick_many_u(k)

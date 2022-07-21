from typing import Iterable

class RotatingBufferList:
    def __init__(self, size : int, initial_value : Iterable, filler = None):
        self.filler = filler
        self._size = size
        self._mem = [filler for _ in range(size)]
        self._ptr = 0
        self._clock = 0
        self.extend(initial_value)
    
    @property
    def size(self):
        """
        Length of the buffer
        """
        return self._size

    @property
    def rounds(self):
        """
        Number of times the buffer size has been exhausted
        """
        return self._clock
    
    @property
    def unreal_length(self):
        """
        Number of items that has been pushed into the array
        (popped won't count)
        """
        return self._ptr + self._clock * self._size

    def empty_items(self):
        """
        Indexes of items that equal filler
        """
        return [
            i for i, itm in
            enumerate(self) if itm == self.filler
        ]

    def non_empty_items(self):
        """
        Items of items that not equal filler 
        """
        return [
            i for i, itm in
            enumerate(self) if itm != self.filler
        ]

    def extend(self, *args):
        """
        Unpack each argument, then proceed to append
        each item of the iterables
        """
        for arg in args:
            self._extend(arg)

    def append(self, arg):
        """
        Append an element to the buffer.
        If the buffer size is exceeded
        the eldest elements will be replaced
        """
        self._append(arg)
    
    def push(self, *args):
        """
        Append each argument.
        It's literally calling :method append:
        for each argument passed
        """
        for arg in args:
            self._append(arg)
    
    def write(self, *args):
        """
        Alias of :method push:
        """
        return self.push(*args)
    
    def pop(self):
        """
        Return the last item and replace it 
        with the buffer filler
        """
        return self._pop()
    
    def extract(self, n):
        """
        Return a list of length :param n int: 
        cycling the buffered items
        """
        return [
            self.__getitem__(i) 
            for i in range(n)
        ]
    
    def infinite_iterator(self):
        """
        Return an iterator that will keep cycling the buffer
        """
        return Pointer(self, infinite = True).__iter__()
    
    def clear(self):
        """
        Replace all the buffer memory with the filler
        """
        return self.fill(self.filler, force = True)
    
    def fill(self, with_, force = False):
        """
        Fill the buffer memory with :param with_:
        If not forced, the :method fill: will only operate
        on empty items (ie items which match the filler)
        """
        if force:
            for i in range(len(self._mem)):
                self._mem[i] = with_
        else:
            for i in range(len(self._mem)):
                if self._mem[i] == self.filler:
                    self._mem[i] = with_
    
    def _first_index(self):
        return self._ptr if self._clock else 0
    
    def _decrement_ptr(self):
        if self._ptr == 0:
            self._clock -= 1
        self._ptr = self._prev_ptr(self._ptr)
    
    def _increment_ptr(self):
        self._ptr = self._next_ptr(self._ptr)
        if self._ptr == 0:
            self._clock += 1
    
    def _next_ptr(self, ptr):
        return (ptr + 1) % self._size
    
    def _prev_ptr(self, ptr):
        return (ptr - 1) % self._size
    
    def _extend(self, iterable):
        for item in iterable:
            self._append(item)
    
    def _append(self, arg):
        self._mem[self._ptr] = arg
        self._increment_ptr()
    
    def _pop(self):
        self._decrement_ptr()
        item = self._mem[self._ptr]
        self._mem[self._ptr] = self.filler
        return item
    
    def __len__(self):
        """
        Size of the inner memory that is helding the buffer. Should be == :property size:
        """
        return len(self._mem)
    
    def __iter__(self):
        """
        Normal iterator: will yield just for the buffer size then StopIteration
        """
        return Pointer(self).__iter__()

    def __getitem__(self, index):
        """
        Can safely be used like a list, accessing with [:param index:]
        the items will always start from the eldest (:index: = 0) to the newest.
        If :index: exceed buffer size, it will cycle back.
        """
        if isinstance(index, slice):
            step = index.step or 1
            start = index.start if index.start is not None else \
                    0 if step > 0 else \
                    self._size - 1
            stop = index.stop if index.stop is not None else \
                    -1 if step < 0 else \
                    self._size
            return [
                self.__getitem__(i) 
                for i in range(start, stop, step)
            ]
        
        return self._mem[self._next_ptr(
            self._first_index() + index - 1
        )]

    def __repr__(self):
        return f"[{', '.join([item.__repr__() for item in self])}]"


class Pointer:
    """
    Necessary class to implement correct iteration
    check https://mail.python.org/pipermail/tutor/2006-January/044455.html
    """
    def __init__(self, rbl : RotatingBufferList, infinite : bool = False):
        self._data = rbl
        self._infinite = infinite
        
    def __iter__(self):
        rl = self._data
        ptr = rl._first_index()
        
        def item():
            nonlocal ptr, rl
            item = rl._mem[ptr]
            ptr = rl._next_ptr(ptr)
            return item
        
        if self._infinite:
            while True: 
                yield item()
        else:
            for _ in range(rl._size):
                yield item()
                
                
"""

###
# use case 1
###
# 
# You want to keep a FIXED SIZE BACKLOG
#
##

events = [{'id':'event number ' + str(i)} for i in range(1001)]
fixed_size_backlog = RotatingBufferList(15)
for event in events:
  fixed_size_backlog.push(event)
last_event = fixed_size_backlog[-1] # [-1] will always held the last event
print(last_event)
print(fixed_size_backlog)


###
# use case 2
###
# 
# You want to keep a FIXED SIZE LIFO QUEUE
#
##
todos = [{'id':'todo number ' + str(i)} for i in range(1001)]
n_things_todo = 10
fixed_size_lifo = RotatingBufferList(n_things_todo, todos)
for _ in fixed_size_lifo:
  print("you have done " + fixed_size_lifo.pop()['id'])
  print(f"only {len(fixed_size_lifo.non_empty_items())} things to do")
  

###
# use case 3
###
# 
# You want to cycle values inside a loop
# just like itertools.cycle()
##

# get the last item after cycling
rhyme = 'Ambarabà cicì cocò tre civette sul comò'
people = ['Gigi', 'Leila', 'Alice', 'Bob', 'Vladimir']
people_cycler = RotatingBufferList(len(people), people).infinite_iterator()
winner = None
for _ in rhyme.split(' '):
  winner = next(people_cycler)
print(winner + " has won the game") # 7 words % 5 people

# use a specific value inside an outer loop
depressing_day = [
    'wake up', 'work in the morning', 'eat lunch', 
    'work in the afternoon', 'eat dinner', 'go to bed'
]
depressing_routine = RotatingBufferList(
    len(depressing_day),
    depressing_day
).infinite_iterator()
health = 1000
days = 1
while health:
  action = next(depressing_routine)
  if action.startswith('eat'):
    health += 5
    print('At least I east something...', '+5', health)
  elif action == 'go to bed':
    health += 10
    print('Good night', '+10', health)
  elif action == 'wake up':
    days += 1
    print(f'---- Day {days} begins -----')
    health -= 1
    print('I feel already depressed', '-1', health)
  elif 'work' in action:
    health -= 12
    print('Work for the boss... yayyy', '-12', health)
print(f"I need to change my routine. I'm exhausted after {days} days of this shit")
"""

"""
  This Module will test empirically the Monty Hall Paradox
  usage:
      python monty_hall.py

  moral:
      - don't ignore the past.
      - if you're offered a deal that has less chance to be bad for you than the one you took before: take it.
"""

from os import urandom
from collections import Counter


def rnd(i: int) -> int:
    assert i < 257
    return int(urandom(1)[0] % i)


def test(func, times: int = 100_000):
    return Counter([func() for _ in range(times)])


def setup_doors(n: int):
    doors = [0] * n
    car_i = rnd(n)
    doors[car_i] = 1
    return doors


def free_check(doors, choice):
    empty_checkable_doors = []
    for i, d in enumerate(doors):
        if i == choice:
            continue
        if d == 1:
            continue
        empty_checkable_doors.append(i)
    return empty_checkable_doors[rnd(len(empty_checkable_doors))]


def play(change: bool = False, nd: int = 3, ignore_past: bool = False):
    doors = setup_doors(nd)
    # print(f"Here are the {nd} closed doors")

    first_choice = rnd(nd)
    # print(f"You choose the door number {first_choice + 1}")

    open_free = free_check(doors, first_choice)
    # print(f"The door {open_free + 1} equal {doors[open_free]}")

    if ignore_past == True:
        can_still_be_opened = [
            i for i in range(nd)
            if not i in [open_free]
        ]
        return doors[
            can_still_be_opened[
                rnd(len(can_still_be_opened))
            ]
        ]

    if change == False:
        return doors[first_choice]

    can_still_be_opened = [
        i for i in range(nd)
        # since you're not ignoring the past
        # you don't want your first choice
        if not i in [first_choice, open_free]
    ]
    n_unchosed_closed_doors = len(can_still_be_opened)
    return doors[
        can_still_be_opened[
            rnd(n_unchosed_closed_doors)
        ]
    ]


if __name__ == "__main__":
    print(
        "If not changing the door:",
        test(lambda: play())
    )
    print(
        "If changing the door:    ",
        test(lambda: play(change=True))
    )
    print(
        "If you ignore the past:  ",
        test(lambda: play(ignore_past=True))
    )

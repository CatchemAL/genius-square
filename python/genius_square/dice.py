import random
from enum import Enum, auto
from itertools import product
from typing import Generator, Self


class DieType(Enum):
    DIE1 = auto()
    DIE2 = auto()
    DIE3 = auto()
    DIE4 = auto()
    DIE5 = auto()
    DIE6 = auto()
    DIE7 = auto()


class Side:
    __slots__ = ["value"]

    def __init__(self, side: str | int) -> None:
        if isinstance(side, str):
            self.value = self._str_to_int(side)
        else:
            self.value = side

    def __int__(self) -> int:
        return self.value

    def __add__(self, other: Self) -> int:
        return self.value + int(other)

    def __radd__(self, other: Self) -> int:
        return int(other) + self.value

    def __str__(self) -> str:
        return self._int_to_str(self.value)

    def __repr__(self) -> str:
        side_str = str(self)
        return f'Side("{side_str}")'

    @staticmethod
    def _str_to_int(side: str) -> int:
        assert len(side) == 2
        assert side[0] in "ABCDEF"
        assert side[1] in "123456"
        letter, number = side[0], int(side[1])
        i, j = 5 - ord(letter) + ord("A"), number - 1
        value = 1 << (i * 8 + j)
        return value

    @staticmethod
    def _int_to_str(value: int) -> str:
        i = 0
        j = 0
        bottom_row = (1 << 6) - 1
        left_column = 1 << 0 | 1 << 8 | 1 << 16 | 1 << 24 | 1 << 32 | 1 << 40

        while value & bottom_row == 0:
            value >>= 8
            i += 1

        while value & left_column == 0:
            value >>= 1
            j += 1

        letter, number = chr(ord("A") + 5 - i), j + 1
        return f"{letter}{number}"

    @classmethod
    def from_bitmask(cls, mask: int) -> list[Self]:
        sides = list[Self]()
        for i in range(6):
            for j in range(6):
                bit = 1 << (i * 8 + j)
                if mask & bit:
                    side = cls(bit)
                    sides.append(side)

        return sides


class Die:
    def __init__(self, side1: str, side2: str, side3: str, side4: str, side5: str, side6: str) -> None:
        side_strs = [side1, side2, side3, side4, side5, side6]
        self.sides = [Side(side_str) for side_str in side_strs]

    def roll(self) -> Side:
        return random.choice(self.sides)

    @classmethod
    def create(cls, die_type: DieType) -> Self:
        sides_by_die = {
            DieType.DIE1: ("A6", "A6", "A6", "F1", "F1", "F1"),
            DieType.DIE2: ("D3", "B4", "C3", "C4", "E3", "D4"),
            DieType.DIE3: ("D1", "D2", "F3", "A1", "E2", "C1"),
            DieType.DIE4: ("B1", "B2", "B3", "A2", "A3", "C2"),
            DieType.DIE5: ("E4", "E5", "F5", "E6", "D5", "F4"),
            DieType.DIE6: ("B5", "C5", "F6", "D6", "A4", "C6"),
            DieType.DIE7: ("A5", "F2", "A5", "F2", "B6", "E1"),
        }

        sides = sides_by_die[die_type]
        return cls(*sides)


class Dice:
    def __init__(self):
        self._dice = [Die.create(die_type) for die_type in DieType]

    def roll(self) -> list[Side]:
        return [die.roll() for die in self._dice]

    def roll_bitmask(self) -> int:
        return sum(int(side) for side in self.roll())

    def roll_all(self) -> Generator[list[Side], None, None]:
        sides0 = {int(side) for side in self._dice[0].sides}
        sides1 = {int(side) for side in self._dice[1].sides}
        sides2 = {int(side) for side in self._dice[2].sides}
        sides3 = {int(side) for side in self._dice[3].sides}
        sides4 = {int(side) for side in self._dice[4].sides}
        sides5 = {int(side) for side in self._dice[5].sides}
        sides6 = {int(side) for side in self._dice[6].sides}

        for combination in product(sides0, sides1, sides2, sides3, sides4, sides5, sides6):
            yield combination

    def roll_all_bitmasks(self) -> list[int]:
        return [sum(sides) for sides in self.roll_all()]

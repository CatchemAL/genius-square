from dataclasses import dataclass
from typing import Self

from .printer import Printer

BITMASK = 0b11111111_11111111_11000000_11000000_11000000_11000000_11000000_11000000


@dataclass(slots=True, frozen=False)
class GameState:
    board: int
    history: list[int]
    available_pieces: list[bool]

    @property
    def is_solved(self) -> bool:
        return len(self.history) == 9

    @staticmethod
    def create_bitboard() -> int:
        # Manual computation of BITMASK constant
        mask = 0
        bitboard = (1 << 64) - 1
        for row in range(6):
            row_mask = (1 << 6) - 1
            row_mask <<= row * 8
            mask |= row_mask

        return bitboard - mask

    def print(self) -> None:
        Printer().print(self.board, self.history)

    @classmethod
    def initial(cls, blocker_mask: int) -> Self:
        # board = cls.create_bitboard()
        return cls(BITMASK | blocker_mask, [], [True] * 9)

    def __repr__(self) -> str:
        return Printer().str_repr(self.board, self.history)

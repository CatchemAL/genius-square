from .printer import Printer

BITMASK = 0b11111111_11111111_11000000_11000000_11000000_11000000_11000000_11000000


class GameState:
    __slots__ = ["board", "history", "available_pieces"]

    def __init__(self, blocker_mask: int) -> None:
        self.board = BITMASK | blocker_mask
        self.history = list[int]()
        self.available_pieces = [True] * 9

    board: int
    history: list[int]
    available_pieces: list[bool]

    @property
    def is_solved(self) -> bool:
        return len(self.history) == 9

    def print(self) -> None:
        Printer().print(self.board, self.history)

    def __repr__(self) -> str:
        return Printer().str_repr(self.board, self.history)

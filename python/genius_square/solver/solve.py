import random
import time
from dataclasses import dataclass
from enum import Enum, auto
from itertools import product
from typing import Self

from tqdm import tqdm

from ._solve import hello_from_bin

BITMASK = 0b11111111_11111111_11000000_11000000_11000000_11000000_11000000_11000000


class Side:
    __slots__ = ["value"]

    def __init__(self, side: str) -> None:
        self.value = self._str_to_int(side)

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


class DieType(Enum):
    DIE1 = auto()
    DIE2 = auto()
    DIE3 = auto()
    DIE4 = auto()
    DIE5 = auto()
    DIE6 = auto()
    DIE7 = auto()


class Die:
    def __init__(self, side1: str, side2: str, side3: str, side4: str, side5: str, side6: str) -> None:
        side_strs = [side1, side2, side3, side4, side5, side6]
        self.sides = [Side(side_str) for side_str in side_strs]

    def roll(self) -> Side:
        return random.choice(self.sides)

    @classmethod
    def create(cls, die_type: DieType) -> Self:
        match die_type:
            case DieType.DIE1:
                return cls("A6", "A6", "A6", "F1", "F1", "F1")
            case DieType.DIE2:
                return cls("D3", "B4", "C3", "C4", "E3", "D4")
            case DieType.DIE3:
                return cls("D1", "D2", "F3", "A1", "E2", "C1")
            case DieType.DIE4:
                return cls("B1", "B2", "B3", "A2", "A3", "C2")
            case DieType.DIE5:
                return cls("E4", "E5", "F5", "E6", "D5", "F4")
            case DieType.DIE6:
                return cls("B5", "C5", "F6", "D6", "A4", "C6")
            case DieType.DIE7:
                return cls("A5", "F2", "A5", "F2", "B6", "E1")
            case _:
                raise ValueError("Invalid die type")


class Dice:
    def __init__(self):
        self._dice = [Die.create(die_type) for die_type in DieType]

    def roll(self) -> list[Side]:
        return [die.roll() for die in self._dice]

    def combinations(self) -> list[int]:
        sides0 = {int(side) for side in self._dice[0].sides}
        sides1 = {int(side) for side in self._dice[1].sides}
        sides2 = {int(side) for side in self._dice[2].sides}
        sides3 = {int(side) for side in self._dice[3].sides}
        sides4 = {int(side) for side in self._dice[4].sides}
        sides5 = {int(side) for side in self._dice[5].sides}
        sides6 = {int(side) for side in self._dice[6].sides}

        blockers = [
            sum(combination)
            for combination in product(sides0, sides1, sides2, sides3, sides4, sides5, sides6)
        ]

        return blockers


class PieceType(Enum):
    SQUARE = 0
    BAR4 = 1
    T = 2
    Z = 3
    L4 = 4
    BAR3 = 5
    L3 = 6
    BAR2 = 7
    DOT = 8

    @classmethod
    def permutations_by_piece(cls) -> dict[Self, list[int]]:
        return {
            PieceType.SQUARE: [771],
            PieceType.BAR4: [15, 16843009],
            PieceType.T: [519, 66305, 65921, 897],
            PieceType.Z: [1539, 131841, 387, 33153],
            PieceType.L4: [263, 1031, 1793, 65795, 131587, 196865, 98561, 449],
            PieceType.BAR3: [7, 65793],
            PieceType.L3: [259, 515, 769, 385],
            PieceType.BAR2: [3, 257],
            PieceType.DOT: [1],
        }


@dataclass(slots=True, frozen=True)
class Piece:
    piece_type: PieceType
    permutations: list[int]


@dataclass(slots=True, frozen=False)
class GameState:
    board: int
    history: list[int]
    available_pieces: list[bool]

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

    @classmethod
    def initial(cls, blockers: int) -> Self:
        # board = cls.create_bitboard()
        return cls(BITMASK + blockers, [], [True] * 9)


class Solver:
    def __init__(self) -> None:
        self.pieces = self.create_pieces()

    def solve(self, state: GameState) -> GameState:
        if self._solve(state, position=0):
            return state

        raise ValueError("No solution found")

    def _solve(self, state: GameState, position: int) -> bool:
        while state.board & (1 << position) > 0:
            position += 1
            if position >= 64:
                return False

        for piece in self.pieces:
            piece_idx = piece.piece_type.value

            if not state.available_pieces[piece_idx]:
                continue

            for permutation in piece.permutations:
                pos_permutation = permutation << position
                if (state.board & pos_permutation) > 0:
                    # The piece cannot be placed
                    continue

                # Place the piece
                state.board |= pos_permutation
                state.history.append(pos_permutation)
                state.available_pieces[piece_idx] = False

                # All pieces have been placed
                if len(state.history) == 9:
                    return True

                # Recurse...
                if self._solve(state, position):
                    return True

                # Backtrack
                state.board &= ~pos_permutation
                state.history.pop()
                state.available_pieces[piece_idx] = True

        return False

    @staticmethod
    def create_pieces() -> list[Piece]:
        permutations_by_piece = PieceType.permutations_by_piece()

        pieces = list[Piece]()
        for piece_type, permutations in permutations_by_piece.items():
            piece = Piece(piece_type, permutations)
            pieces.append(piece)

        return sorted(pieces, key=lambda x: x.piece_type.value)


class Printer:
    BOTTOM_ROW = (1 << 6) - 1
    LEFT_COLUMN = 1 << 0 | 1 << 8 | 1 << 16 | 1 << 24 | 1 << 32 | 1 << 40

    def __init__(self) -> None:
        pass

    def print(self, state: GameState) -> str:
        grid = [None] * 8
        for i in range(8):
            grid[i] = [None] * 8

        board = state.board
        for move in state.history:
            board &= ~move
            piece_type = self._identify_piece(move)

            for i in range(8):
                for j in range(8):
                    if move & (1 << (i * 8 + j)) > 0:
                        grid[i][j] = piece_type

        grid = grid[-3::-1]

        color_by_piece_type = {
            PieceType.SQUARE: "🟩",
            PieceType.BAR4: "⬜️",
            PieceType.T: "🟨",
            PieceType.L4: "🟦",
            PieceType.Z: "🟥",
            PieceType.BAR3: "🟧",
            PieceType.L3: "🟪",
            PieceType.BAR2: "🟫",
            PieceType.DOT: "⬛️",
        }

        # Banner
        print("✨✨✨✨✨✨✨✨")
        print(" GENIUS SQUARE")
        print()

        # Now print the grid
        print("  1 2 3 4 5 6")
        for i in range(6):
            char = chr(ord("A") + i)
            print(f"{char} ", end="")
            for j in range(6):
                if grid[i][j] is not None:
                    piece_type = grid[i][j]
                    marker = color_by_piece_type[piece_type]
                    print(marker, end="")
                elif board & (1 << ((5 - i) * 8 + j)) > 0:
                    print("👽", end="")
                else:
                    print("  ", end="")
            print()
        pass

    def _identify_piece(self, move: int) -> PieceType:
        while move & self.BOTTOM_ROW == 0:
            move >>= 8
        while move & 1 == 0:
            move >>= 1

        permutations_by_piece = PieceType.permutations_by_piece()

        for piece_type, permutations in permutations_by_piece.items():
            for permutation in permutations:
                if move & permutation == permutation:
                    return piece_type


def solve() -> str:
    dice = Dice()
    sides = dice.roll()
    blockers = sum(sides)

    solver = Solver()
    printer = Printer()

    print("Setup:")
    print(" - " + ", ".join(map(str, sides)))
    print()
    state = GameState.initial(blockers)

    solver.solve(state)
    printer.print(state)

    print("\nSolved! ✨")


def solve() -> str:
    dice = Dice()
    all_blockers = dice.combinations()

    solver = Solver()

    for blockers in tqdm(all_blockers):
        state = GameState.initial(blockers)
        solver.solve(state)

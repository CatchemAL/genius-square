from dataclasses import dataclass
from typing import Self

from .pieces import PieceType

BITMASK = 0b11111111_11111111_11000000_11000000_11000000_11000000_11000000_11000000


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
    def initial(cls, blocker_mask: int) -> Self:
        # board = cls.create_bitboard()
        return cls(BITMASK + blocker_mask, [], [True] * 9)


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

from dataclasses import dataclass
from enum import Enum
from typing import Self


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

    @classmethod
    def create_pieces(cls) -> list[Self]:
        permutations_by_piece = PieceType.permutations_by_piece()

        pieces = list[Self]()
        for piece_type, permutations in permutations_by_piece.items():
            piece = cls(piece_type, permutations)
            pieces.append(piece)

        return sorted(pieces, key=lambda x: x.piece_type.value)

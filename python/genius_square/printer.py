from .pieces import PieceType


class Printer:
    BOTTOM_ROW = (1 << 6) - 1
    LEFT_COLUMN = 1 << 0 | 1 << 8 | 1 << 16 | 1 << 24 | 1 << 32 | 1 << 40

    @classmethod
    def str_repr(cls, board_mask: int, history: list[int]) -> str:
        grid = [None] * 8
        for i in range(8):
            grid[i] = [None] * 8

        board = board_mask
        for move in history:
            board &= ~move
            piece_type = cls._identify_piece(move)

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
        lines = list[str]()
        lines.append("  1 2 3 4 5 6")

        # Now print the grid
        for i in range(6):
            char = chr(ord("A") + i)
            row = f"{char} "
            for j in range(6):
                if grid[i][j] is not None:
                    piece_type = grid[i][j]
                    marker = color_by_piece_type[piece_type]
                    row += marker
                elif board & (1 << ((5 - i) * 8 + j)) > 0:
                    row += "👽"
                else:
                    row += "🫥"
            lines.append(row)

        return "\n".join(lines)

    def print(self, board_mask: int, history: list[int]) -> None:
        str_repr = self.str_repr(board_mask, history)
        print("✨✨✨✨✨✨✨✨")
        print(" GENIUS SQUARE\n")
        print(str_repr)

    @classmethod
    def _identify_piece(cls, move: int) -> PieceType:
        while move & cls.BOTTOM_ROW == 0:
            move >>= 8
        while move & 1 == 0:
            move >>= 1

        permutations_by_piece = PieceType.permutations_by_piece()

        for piece_type, permutations in permutations_by_piece.items():
            for permutation in permutations:
                if move & permutation == permutation:
                    return piece_type

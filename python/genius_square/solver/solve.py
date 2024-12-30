from ..pieces import Piece, PieceType
from ..state import GameState
from ._solve import hello_from_bin


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

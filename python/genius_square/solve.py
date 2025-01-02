from .pieces import Piece
from .state import GameState

PIECES = Piece.create_pieces()


class Counter:
    count: int = 0


class Solver:
    def __init__(self) -> None:
        self.pieces = PIECES

    def solve(self, state: GameState) -> GameState:
        if self._solve(state, position=0):
            return state
        raise ValueError("No solution found")

    def count_solns(self, state: GameState) -> int:
        counter = Counter()
        self._solve(state, position=0, soln_count=counter)
        return counter.count

    def _solve(self, state: GameState, position: int, soln_count: Counter | None = None) -> bool:
        while state.board & (1 << position) > 0:
            position += 1
            if position >= 48:
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

                if state.is_solved:
                    if soln_count is None:
                        # We're not counting solutions, so we can return early
                        return True
                    # Solution found, increment counter then backtrack
                    soln_count.count += 1
                # Not solved so we must recurse...
                elif self._solve(state, position, soln_count):
                    return True

                # Backtrack
                state.board &= ~pos_permutation
                state.history.pop()
                state.available_pieces[piece_idx] = True

        return False

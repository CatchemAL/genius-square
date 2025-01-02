use pyo3::prelude::*;

use crate::{pieces::Piece, state::GameState};

#[pyclass]
pub struct Solver {
    pieces: Vec<Piece>,
}

#[pymethods]
impl Solver {
    #[new]
    pub fn new() -> Self {
        let pieces = Piece::pieces();
        Self { pieces }
    }

    pub fn solve(&self, state: &mut GameState) -> bool {
        self._solve(state, 0)
    }

    pub fn count_solns(&self, state: &mut GameState) -> u32 {
        let mut counter: u32 = 0;
        self._count_solns(state, 0, &mut counter);
        counter
    }
}

impl Solver {
    fn _solve(&self, state: &mut GameState, mut pos: usize) -> bool {
        while (state.board & (1 << pos)) != 0 {
            pos += 1;
            if pos > 48 {
                return false;
            }
        }

        for piece in &self.pieces {
            if !state.is_available(piece.piece_type) {
                continue;
            }

            for &permutation in &piece.permutations {
                let pos_permutation = permutation << pos;
                if (state.board & pos_permutation) != 0 {
                    // The piece cannot be placed.
                    continue;
                }

                // Place the piece
                state.board |= pos_permutation;
                state.history.push(pos_permutation);
                state.mark_piece_as_used(piece.piece_type);

                if state.is_solved() || self._solve(state, pos) {
                    return true;
                }

                state.board &= !pos_permutation;
                state.history.pop();
                state.mark_piece_as_available(piece.piece_type);
            }
        }

        false
    }

    fn _count_solns(&self, state: &mut GameState, mut pos: usize, counter: &mut u32) {
        while (state.board & (1 << pos)) != 0 {
            pos += 1;
            if pos > 48 {
                return;
            }
        }

        for piece in &self.pieces {
            if !state.is_available(piece.piece_type) {
                continue;
            }

            for &permutation in &piece.permutations {
                let pos_permutation = permutation << pos;
                if (state.board & pos_permutation) != 0 {
                    // The piece cannot be placed.
                    continue;
                }

                // Place the piece
                state.board |= pos_permutation;
                state.history.push(pos_permutation);
                state.mark_piece_as_used(piece.piece_type);

                if state.is_solved() {
                    *counter += 1;
                } else {
                    self._count_solns(state, pos, counter);
                }

                state.board &= !pos_permutation;
                state.history.pop();
                state.mark_piece_as_available(piece.piece_type);
            }
        }
    }
}

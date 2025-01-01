use pyo3::prelude::*;
use std::collections::HashMap;

const NUM_PIECES: usize = 9;
const BITMASK: u64 = 0b11111111_11111111_11000000_11000000_11000000_11000000_11000000_11000000;

#[pyclass(eq, eq_int)]
#[repr(u16)]
#[derive(Copy, Clone, PartialEq, Eq, Hash, Debug)]
pub enum PieceType {
    Square = 1 << 0, // 0b00000000_00000001
    Bar4 = 1 << 1,   // 0b00000000_00000010
    T = 1 << 2,      // 0b00000000_00000100
    Z = 1 << 3,      // 0b00000000_00001000
    L4 = 1 << 4,     // 0b00000000_00010000
    Bar3 = 1 << 5,   // 0b00000000_00100000
    L3 = 1 << 6,     // 0b00000000_01000000
    Bar2 = 1 << 7,   // 0b00000000_10000000
    Dot = 1 << 8,    // 0b00000001_00000000
}

impl PieceType {
    pub fn permutations_by_piece_type() -> HashMap<Self, Vec<u64>> {
        use PieceType::*;
        return HashMap::from([
            (Square, vec![771]),
            (Bar4, vec![15, 16843009]),
            (T, vec![519, 66305, 65921, 897]),
            (Z, vec![1539, 131841, 387, 33153]),
            (L4, vec![263, 1031, 1793, 65795, 131587, 196865, 98561, 449]),
            (Bar3, vec![7, 65793]),
            (L3, vec![259, 515, 769, 385]),
            (Bar2, vec![3, 257]),
            (Dot, vec![1]),
        ]);
    }
}

#[derive(Debug, Clone)]
pub struct Piece {
    piece_type: PieceType,
    permutations: Vec<u64>,
}

impl Piece {
    pub fn new(piece_type: PieceType, permutations: Vec<u64>) -> Self {
        Self {
            piece_type,
            permutations,
        }
    }

    pub fn pieces() -> Vec<Self> {
        let permutations = PieceType::permutations_by_piece_type();

        let mut pieces = Vec::new();
        for (piece_type, permutations) in permutations.into_iter() {
            let piece = Self::new(piece_type, permutations);
            pieces.push(piece);
        }

        pieces
    }
}

#[pyclass]
#[derive(Debug, Clone)]
pub struct GameState {
    pub board: u64,
    available_pieces: u16,
    pub history: Vec<u64>,
}

#[pymethods]
impl GameState {
    #[new]
    pub fn new(blocker_mask: u64) -> Self {
        Self {
            board: blocker_mask & BITMASK,
            available_pieces: 0b1_11111111,
            history: Vec::with_capacity(NUM_PIECES),
        }
    }

    pub fn is_solved(&self) -> bool {
        self.available_pieces == 0
    }

    fn mark_piece_as_used(&mut self, piece_type: PieceType) {
        self.available_pieces &= !(piece_type as u16);
    }

    fn mark_piece_as_available(&mut self, piece_type: PieceType) {
        self.available_pieces |= piece_type as u16;
    }

    fn is_available(&self, piece_type: PieceType) -> bool {
        self.available_pieces & (piece_type as u16) != 0
    }
}

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
}

use pyo3::prelude::*;

use crate::pieces::PieceType;

const NUM_PIECES: usize = 9;
const BITMASK: u64 = 0b11111111_11111111_11000000_11000000_11000000_11000000_11000000_11000000;

#[pyclass(subclass)]
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
            board: blocker_mask | BITMASK,
            available_pieces: 0b1_11111111,
            history: Vec::with_capacity(NUM_PIECES),
        }
    }

    #[getter]
    pub fn board(&self) -> u64 {
        self.board
    }

    #[getter]
    pub fn history(&self) -> Vec<u64> {
        self.history.clone()
    }

    #[getter]
    pub fn is_solved(&self) -> bool {
        self.available_pieces == 0
    }
}

impl GameState {
    pub fn mark_piece_as_used(&mut self, piece_type: PieceType) {
        self.available_pieces &= !(piece_type as u16);
    }

    pub fn mark_piece_as_available(&mut self, piece_type: PieceType) {
        self.available_pieces |= piece_type as u16;
    }

    pub fn is_available(&self, piece_type: PieceType) -> bool {
        self.available_pieces & (piece_type as u16) != 0
    }
}

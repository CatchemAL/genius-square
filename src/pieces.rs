use std::collections::HashMap;

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
    pub piece_type: PieceType,
    pub permutations: Vec<u64>,
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

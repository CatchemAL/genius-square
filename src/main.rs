mod bar;
mod foo;
mod pieces;

use pieces::GameState;
use pieces::Piece;
use pieces::Solver;

fn main() {
    println!("Hello, World!");

    // Calling a module
    let (a, b) = (3, 4);
    let x: i32 = foo::add(a, b);
    println!("{a} + {b} = {x}");

    // Calling another module
    let y = bar::product(a, b);
    println!("{a} * {b} = {y}");

    let z = bar::baz::factorial(b);
    println!("{b}! = {z}");

    let piece_type = pieces::PieceType::Square;
    let permutations = vec![771];
    let piece = Piece::new(piece_type, permutations);

    let pieces = Piece::pieces();

    let blocker_mask: u64 = 35257386926098;
    let mut state = GameState::new(blocker_mask);

    let solver = Solver::new();
    solver.solve(&mut state);

    print!("test");
}

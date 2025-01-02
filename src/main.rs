mod bar;
mod foo;
mod pieces;
mod solver;
mod state;

use solver::Solver;
use state::GameState;

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

    let solver = Solver::new();

    let blocker_mask: u64 = 35257386599434;
    let mut state = GameState::new(blocker_mask);
    let is_solved = solver.solve(&mut state);

    if is_solved {
        let value = state.board;
        println!("The board value is {value}");
    } else {
        println!("Failed to solve...")
    }

    let blocker_mask: u64 = 35257386599434;
    let mut state = GameState::new(blocker_mask);
    let soln_count = solver.count_solns(&mut state);
    println!("Num solutions is {soln_count}");
}

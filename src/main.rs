mod bar;
mod foo;

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
}

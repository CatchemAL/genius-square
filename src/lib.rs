use pyo3::prelude::*;
mod pieces;
mod solver;

#[pyfunction]
fn hello_from_bin() -> String {
    "Hello from genius-square!".to_string()
}

/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
fn _solve(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(hello_from_bin, m)?)?;
    m.add_class::<solver::Counter>()?;
    m.add_class::<pieces::Solver>()?;
    m.add_class::<pieces::GameState>()?;
    Ok(())
}

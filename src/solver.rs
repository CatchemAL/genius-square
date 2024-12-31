use pyo3::prelude::*;

/// A simple class with a counter.
#[pyclass]
pub struct Counter {
    count: i32,
}

#[pymethods]
impl Counter {
    #[new]
    fn new() -> Self {
        Counter { count: 0 }
    }

    fn increment(&mut self) {
        self.count += 1;
    }

    fn get_count(&self) -> PyResult<i32> {
        Ok(self.count)
    }
}

from genius_square.experimental import Counter, hello_from_bin


def test_bindings() -> None:
    x = hello_from_bin()
    assert x == "Hello from genius-square!"


class TestCounter:
    def test_increment(self) -> None:
        counter = Counter()
        counter.increment()
        assert counter.get_count() == 1

    def test_get_count(self) -> None:
        counter = Counter()
        assert counter.get_count() == 0

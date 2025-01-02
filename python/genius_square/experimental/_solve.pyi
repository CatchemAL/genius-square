class GameState:
    def __init__(self, blocker_mask: int) -> None: ...
    @property
    def is_solved(self) -> bool: ...
    @property
    def board(self) -> int: ...
    @property
    def history(self) -> list[int]: ...

class Solver:
    def __init__(self) -> None: ...
    def solve(self) -> bool: ...
    def count_solns(self) -> int: ...

# Ignore - just some random rust functions
def hello_from_bin() -> str: ...

class Counter:
    def increment(self) -> None: ...
    def get_count(self) -> int: ...
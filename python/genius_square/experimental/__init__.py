from ..printer import Printer
from ._solve import Counter, GameState, Solver, hello_from_bin

# Hacky - sorry - time boxed project!
GameState.print = lambda self: Printer().print(self.board, self.history)
GameState.__repr__ = lambda self: Printer().str_repr(self.board, self.history)

__all__ = [
    "Counter",
    "GameState",
    "hello_from_bin",
    "Solver",
]

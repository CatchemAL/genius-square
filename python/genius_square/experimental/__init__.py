from ..printer import Printer
from ._solve import Counter, GameState, Solver, hello_from_bin
from .solver import ExtendedGameState

# Hacky - sorry - time boxed project!
GameState.__repr__ = lambda self: Printer().str_repr(self.board, self.history)

__all__ = [
    "Counter",
    "ExtendedGameState",
    "GameState",
    "hello_from_bin",
    "Solver",
]

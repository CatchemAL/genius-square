from ..printer import Printer
from ._solve import GameState


class ExtendedGameState(GameState):
    def __init__(self, blocker_mask: int) -> None:
        super().__init__()

    def print(self) -> str:
        return Printer().print(self.board_mask, self.history)

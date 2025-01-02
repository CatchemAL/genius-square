from genius_square.experimental import GameState, Solver


class TestSolver:
    def test_increment(self) -> None:
        state = GameState(8937910833153)
        solver = Solver()
        assert solver.solve(state)

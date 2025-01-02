from genius_square import GameState, Solver


class TestSolver:
    def test_increment(self) -> None:
        state = GameState.initial(8937910833153)
        solver = Solver()
        assert solver.solve(state)

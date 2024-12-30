from concurrent.futures import ProcessPoolExecutor
from functools import partial

import click
from tqdm import tqdm

from .dice import Dice, Side
from .solver.solve import Solver
from .state import GameState


@click.command()
@click.option("--sides", default=None, help="CSV of sides (e.g. A6,C3,F3,B3,D5,D6,A5")
@click.option("--mask", default=None, type=int, help="Blocker bitmask")
def solve(sides: str | None, mask: int | None) -> None:
    assert sides is None or mask is None, "Cannot specify both sides and mask"

    if sides:
        sides = sides.split(",")
        sides = [Side(side) for side in sides]
    elif mask:
        sides = Side.from_bitmask(mask)
    else:
        dice = Dice()
        sides = dice.roll()

    print("Setup:")
    print(" - " + ", ".join(map(str, sides)))
    print()
    blocker_mask = sum(sides)
    state = GameState.initial(blocker_mask)

    solver = Solver()
    solver.solve(state)
    state.print()

    print("\nSolved! ✨")


@click.command()
def benchmark() -> None:
    dice = Dice()
    solver = Solver()
    s = partial(solve_mask, solver=solver)
    masks = dice.all_bitmasks()
    with ProcessPoolExecutor() as executor:
        list(tqdm(executor.map(s, masks, chunksize=100), total=len(masks)))


def solve_mask(mask: int, solver: Solver) -> None:
    state = GameState.initial(mask)
    solver.solve(state)


@click.group()
def gs_cli():
    pass


gs_cli.add_command(benchmark, "benchmark")
gs_cli.add_command(solve, "solve")

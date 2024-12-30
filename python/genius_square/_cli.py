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
def count(sides: str | None, mask: int | None) -> None:
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
    count = solver.count_solns(state)
    print(f"Number of solutions: {count:,}")


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
    fn = partial(solve_mask, solver=solver)
    masks = dice.all_bitmasks()
    with ProcessPoolExecutor() as executor:
        list(tqdm(executor.map(fn, masks, chunksize=64), total=len(masks)))


@click.command()
@click.option("--file", default="data/solutions.csv", help="File to write solutions to")
def all_counts(file: str) -> None:
    dice = Dice()
    solver = Solver()
    fn = partial(count_mask, solver=solver)
    masks = dice.all_bitmasks()
    with ProcessPoolExecutor() as executor:
        results = list(tqdm(executor.map(fn, masks, chunksize=32), total=len(masks)))
        results = sorted(results, key=lambda x: x[1])

    csv = "mask,soln_count\n" + "\n".join([f"{mask},{count}" for mask, count in results])
    with open(file, "w") as f:
        f.write(csv)

    # Print head and tail of results
    print("+-----------------+------------+")
    print("| mask            | soln_count |")
    print("+------------- ---+------------+")
    for mask, count in results[:5]:
        print(f"| {mask:<16}| {count:>10,} |")

    print("| ...             |        ... |")
    for mask, count in results[-5:]:
        print(f"| {mask:<16}| {count:>10,} |")
    print("+-----------------+------------+")


def solve_mask(mask: int, solver: Solver) -> None:
    state = GameState.initial(mask)
    solver.solve(state)


def count_mask(mask: int, solver: Solver) -> tuple[int, int]:
    state = GameState.initial(mask)
    soln_count = solver.count_solns(state)
    return mask, soln_count


@click.group()
def gs_cli():
    pass


gs_cli.add_command(benchmark, "benchmark")
gs_cli.add_command(count, "count")
gs_cli.add_command(all_counts, "all-counts")
gs_cli.add_command(solve, "solve")

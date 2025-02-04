from concurrent.futures import ProcessPoolExecutor

import click
from tqdm import tqdm

from .dice import Dice, Side
from .solve import Solver
from .state import GameState


@click.command()
@click.option("--sides", default=None, help="CSV of sides (e.g. A6,C3,F3,B3,D5,D6,A5")
@click.option("--mask", default=None, type=int, help="Blocker bitmask")
@click.option("--rust", default=False, is_flag=True, help="Whether to use the rust engine.")
def solve(sides: str | None, mask: int | None, rust: bool) -> None:
    if rust:
        from .experimental import GameState, Solver
    else:
        from . import GameState, Solver

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
    blocker_mask: int = sum(sides)
    state = GameState(blocker_mask)

    solver = Solver()
    solver.solve(state)
    state.print()

    print("\nSolved! ✨")


@click.command()
@click.option("--sides", default=None, help="CSV of sides (e.g. A6,C3,F3,B3,D5,D6,A5")
@click.option("--mask", default=None, type=int, help="Blocker bitmask")
@click.option("--rust", default=False, is_flag=True, help="Whether to use the rust engine.")
def count_solns(sides: str | None, mask: int | None, rust: bool) -> None:
    if rust:
        from .experimental import GameState, Solver
    else:
        from . import GameState, Solver
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
    state = GameState(blocker_mask)

    solver = Solver()
    count = solver.count_solns(state)
    print(f"Number of solutions: {count:,}")


@click.command()
@click.option("--rust", default=False, is_flag=True, help="Whether to use the rust engine.")
def benchmark(rust: bool) -> None:
    dice = Dice()
    fn = solve_mask_rust if rust else solve_mask
    masks = dice.all_bitmasks()

    with ProcessPoolExecutor() as executor:
        list(tqdm(executor.map(fn, masks, chunksize=128), total=len(masks)))


@click.command()
@click.option("--file", default="data/solutions.csv", help="File to write solutions to")
@click.option("--rust", default=False, is_flag=True, help="Whether to use the rust engine.")
def all_counts(file: str, rust: bool) -> None:
    dice = Dice()
    fn = count_mask_rust if rust else count_mask
    masks = dice.all_bitmasks()
    with ProcessPoolExecutor() as executor:
        results = list(tqdm(executor.map(fn, masks, chunksize=64), total=len(masks)))
        results = sorted(results, key=lambda x: (x[1], x[0]))

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


def solve_mask(mask: int) -> None:
    solver = Solver()
    state = GameState(mask)
    solver.solve(state)


def count_mask(mask: int) -> tuple[int, int]:
    solver = Solver()
    state = GameState(mask)
    soln_count = solver.count_solns(state)
    return mask, soln_count


def solve_mask_rust(mask: int) -> None:
    from .experimental import GameState, Solver

    solver = Solver()
    state = GameState(mask)
    solver.solve(state)


def count_mask_rust(mask: int) -> tuple[int, int]:
    from .experimental import GameState, Solver

    solver = Solver()
    state = GameState(mask)
    soln_count = solver.count_solns(state)
    return mask, soln_count


@click.group()
def gs_cli():
    pass


gs_cli.add_command(solve, "solve")
gs_cli.add_command(benchmark, "benchmark")
gs_cli.add_command(all_counts, "all-counts")
gs_cli.add_command(count_solns, "count")

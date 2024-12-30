## Genius-Square
A fast solver for the game Genius Square written in Python and Rust.

The package comes with a CLI tool and Python API.
### CLI Tool
```bash
# Using the solve interface
genius-square solve        
genius-square solve --sides=F1,D4,A1,B2,E6,C5,F2
genius-square solve --mask=35257386599434

# Solve all problems
genius-square benchmark

# Get the number of valid solutions for all configurations
genius-square all-counts
```

### Python API
See the notebooks demo for examples.
```python
# First we take a random roll of the dice.
dice = Dice()
sides = dice.roll()

# Visualise the board with just the blockers
blocker_mask = sum(sides)
state = GameState.initial(blocker_mask)
state

# Now we solve the game and redisplay the state.
solver = Solver()
solver.solve(state)
state


  1 2 3 4 5 6
A ⬜️⬜️⬜️⬜️👽👽
B 👽🟦🟧🟧🟧🟫
C 🟪🟦🟦🟦🟨🟫
D 🟪🟪👽🟨🟨🟨
E 🟩🟩⬛️👽🟥🟥
F 🟩🟩👽🟥🟥👽
```




### Speed
The package solves the 62,208 puzzles in about 1.8 seconds on my laptop (MacBook Pro 2023), averaging 36k solves per second.
```bash
/workspaces/genius-square (main) $ genius-square benchmark
100%|█████████| 62208/62208 [00:01<00:00, 36138.80it/s]
```
All possible solutions for all possible configurations takes 26 minutes.
```bash
100%|██████████| 62208/62208 [26:04<00:00, 39.77it/s] 
```

The package utilises:
- Very efficient/compact bitboard representations to manipulate pieces and check validity
- Sensible ordering of pieces - large-to-small with low permutation pieces first
- Concurrency

Illustration of the `GameState` class.
```python
@dataclass(slots=True, frozen=False)
class GameState:
    board: int
    history: list[int]
    available_pieces: list[bool]
```

The board is initialised as a 64-bit integer as shown below. This corresponds to the example above with the 7 blockers already played:
```
1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1
0 0 0 0 1 1 1 1
1 0 0 0 0 0 1 1
0 0 0 0 0 0 1 1
0 0 1 0 0 0 1 1
0 0 0 1 0 0 1 1
0 0 1 0 0 1 1 1
```
The history of pieces played follows a similar philosphy.

### Game Stats
- Num combinations: 62,208
- Fewest solns: 11 (mask=35257386599434)
- Most solns: 22,317 (mask=67070209297408)
- Median solns: 1,340
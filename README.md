## Genius-Square
An extremely fast solver for the game [Genius Square](https://www.happypuzzle.co.uk/family-puzzles-and-games/the-genius-collection/genius-square) written in Python and Rust.

The package comes with a CLI tool and a Python API.
### CLI Tool
```bash
# Using the solve interface
genius-square solve        
genius-square solve --sides=F1,D4,A1,B2,E6,C5,F2
genius-square solve --mask=35257386599434

# Solve all problems
genius-square benchmark
genius-square benchmark --rust

# Get the number of valid solutions for all configurations
genius-square all-counts
genius-square all-counts --rust
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




### Speed (pure Python) 🐍
The package solves the 62,208 puzzles in about 1.8 seconds on my laptop (MacBook Pro 2023), averaging 36k solves per second.
```bash
/workspaces/genius-square $ genius-square benchmark
100%|██████████| 62208/62208 [00:01<00:00, 36138.80it/s]
```
All possible solutions for all possible configurations takes 26 minutes.
```bash
/workspaces/genius-square $ genius-square all-counts
100%|██████████| 62208/62208 [26:04<00:00, 39.77it/s] 
```

### Speed (Rust engine) 🦀
Rust provides a x60 speedup and solves all problems in 0.1 seconds.
```bash
/workspaces/genius-square $ genius-square benchmark --rust
100%|██████████| 62208/62208 [00:00<00:00, 405135.26it/s]
```
To find all possible solutions to all possible configurations takes 25 seconds.
```bash
/workspaces/genius-square $ genius-square all-counts --rust
100%|██████████| 62208/62208 [00:25<00:00, 2399.41it/s]
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

<img src="https://github.com/CatchemAL/genius-square/blob/main/data/distribution.png?raw=true" width="420">

## Going beyond the game
### Insanely hard mode
We can forego the dice and instead ask, "are there any configurations of the board with only one solution?". This is quite a step up in complexity - there are $36C7 = 8,347,680$ mask configurations and we want to count the number of solutions to each configuration. The average number of solutions per configuration is 1,364, so this requires us to find 11,387,941,312 solution. On my laptop, this takes 48 minutes.

```
100%|██████████| 8347680/8347680 [48:42<00:00, 2856.61it/s] 
```


Here is one such configuration. Can you solve it?

```
🫥🫥🫥🫥🫥🫥
🫥🔘🫥🫥🔘🫥
🔘🫥🫥🫥🫥🔘
🫥🫥🫥🫥🫥🫥
🫥🔘🫥🫥🔘🫥
🫥🫥🔘🫥🫥🫥
```

<details>
  <summary>Solution</summary>

  ```
  🟫🟨🟨🟨🟪🟪
  🟫🔘🟨⬜️🔘🟪
  🔘🟩🟩⬜️🟥🔘
  🟦🟩🟩⬜️🟥🟥
  🟦🔘⬛️⬜️🔘🟥
  🟦🟦🔘🟧🟧🟧
  ```

</details>


And here is an [overview of all 800 puzzles](https://github.com/CatchemAL/genius-square/blob/main/data/Genius%20Square%20-%20Insanely%20Hard%20Mode.pdf) with only one solution. Answers at the bottom.

### Stats for nerds
- Number of unsolvable configurations: 172,440
- Number of solutions with:
  - 1 solution: 800
  - 2 solutions: 1,324
  - 3 solutions: 1,328
  - ...
  - 100,593 solutions: 16
- Median number of solutions: 719


<details>
  <summary>The easiest configuration conceivable</summary>
  This has 100,593 solutions. Can you find one? I believe in you. You can do anything if you put your mind to it.

  ```
  🔘🔘🔘🔘🔘🔘
  🔘🫥🫥🫥🫥🫥
  🫥🫥🫥🫥🫥🫥
  🫥🫥🫥🫥🫥🫥
  🫥🫥🫥🫥🫥🫥
  🫥🫥🫥🫥🫥🫥
  ```

</details>
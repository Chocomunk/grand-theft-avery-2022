# Avery OS

## Setup/Installation

Make sure you have python3/pip installed and ideally a fresh virtual environment.
In the `averyos/` directory, run:

```bash
python -m pip install -r requirements.txt
```

**NOTE:** the `python` command in the line above must point to the correct python 
interpreter.

## Usage

To run locally, simply call `python main.py`. This will run the puzzle/filesystem
for the *Grand Theft Avery* Ditch Day 2022 stack.

**NOTE:** Physical hints for this puzzle are stored in `puzzle/dday_puzzle/room-objects/`.

Not all physical aspects are added to the repository yet. Specifically, the `Office`
puzzles and final puzzle do not have the full hints.

You can define your own filesystem (`puzzle/` folder for examples) and run a 
shell on it as shown in `main.py`
<!-- 
## Development

### General coding philosophy

Try to separate the OS design and the puzzle design/solutions. Ideally link
the two using concrete designs/ideas (e.g. locks), or by using callbacks. This
allows the OS to be decoupled from any specific puzzle designs.

**NOTE**: The above goal won't always be possible, but we can try our best.

### Todo

- Puzzles
  - [ ] Make tutorial puzzle
- GUI
  - [ ] Make all the margins/padding line up
  - Terminal GUI
    - [ ] Scrolling past the end
    - [ ] Clean up color and font handling
      - Color for prompt?
  - `ls` GUI
    - [ ] Add section headers/titles
    - [ ] Add icons
  - `map` GUI (`render`)
    - [ ] Make minimap
  - `cat` GUI
    - [ ] Make it pretty?
    - [ ] Remove added test text
  - `unlock` GUI
    - [ ] Multiple passwords for a node
    - [ ] Make it pretty
- Shell
  - [ ] Add input pre-processing callbacks -->

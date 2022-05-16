# Avery OS

## Usage

To run locally, simply call `python main.py`, and a shell instance and example
file system will be started.

You can define your own filesystem (`puzzle/` folder for examples) and run a 
shell on it as shown in `main.py`

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
  - [ ] Add input pre-processing callbacks

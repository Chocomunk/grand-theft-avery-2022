# Avery OS

## Usage

To run locally, simply call `python main.py`, and a shell instance and example
file system will be started.

You can define your own filesystem setup (`filesystem_gen.py`) and run a shell 
on it as shown in `main.py`

## Development

### General coding philosophy

Try to separate the OS design and the puzzle design/solutions. Ideally link
the two using concrete designs/ideas (e.g. locks), or by using callbacks. This
allows the OS to be decoupled from any specific puzzle designs.

**NOTE**: The above goal won't always be possible, but we can try our best.

### Todo

- [ ] Start Puzzle state webserver
  - AveryOS backend send puzzle state to webserver.
  - Webserver serves (mobile-friendly) websites to users and forwards user interactions
    back to the AveryOS backend.
- Puzzles
  - [ ] Make tutorial puzzle
  - [ ] Write a function to convert an adjacency matrix and a list of names to a
        FS graph.
- File System
  - [ ] Keep track of whether nodes are visited.
    - Also consider keeping track of whether all of a node's connections are
      visited (both child+parent? or separately?)
- GUI
  - [ ] Make all the margins/padding line up
  - Terminal GUI
    - [ ] Scrolling past the end
    - [ ] Clean up color and font handling
      - Color for prompt?
  - `ls` GUI
    - Call `ls` to toggle a "Directory" pane on the LHS
    - Cannot be shown with `map`
    - [ ] Add section headers/titles
    - [ ] Add icons
  - `map` GUI (`render`)
    - Call `map` to toggle either a "Map" view or pane.
    - Cannot be shown with `ls`
    - [ ] Fix radius scaling
    - [ ] Make minimap
  - `cat` GUI
    - Opens a widget that displays text
    - [ ] Make it pretty?
    - [ ] Remove added test text
  - `unlock` GUI
    - [ ] Pause/animations after answers
    - [ ] Make it pretty
- Shell
  - [ ] Add input pre-processing callbacks

- Misc Ideas:
  - Visibility (similar to locks, but for whether nodes can be seen and navigated)
  - Adding files to the path (or smth similar). Global visibility for some files
  - Alias for commands
  - Store programs per-node rather than per-directory
    - If we allow users to move or link directories, then could have puzzles
      requiring files to be moved to certain nodes for programs to see them.
    - Also good for printing.

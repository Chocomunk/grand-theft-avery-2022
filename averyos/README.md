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
  - [ ] Write a function to convert an adjacency matrix and a list of names to a
        FS graph.
- File System
  - [ ] Keep track of whether nodes are visited.
    - Also consider keeping track of whether all of a node's connections are
      visited (both child+parent? or separately?)
- GUI
  - [x] Make everything fullscreen
  - [x] Add pre-defined window layouts for programs to use
    - Programs can access the surfaces of a specific layout
    - [x] Window "views" that programs can assign
  - [ ] Add `ViewManager` to `OSWindow`
  - [ ] Terminal GUI
    - [ ] Print different log types in different colors
      - Color for prompt?
    - [ ] Allow scrolling over lines
      - Stop doing line moving in a sussy way
    - [ ] Allow up/down arrows to get last/next in command history.
  - [ ] Configure gui/__init__.py
  - [ ] `ls` GUI
    - Call `ls` to toggle a "Directory" pane on the LHS
    - Cannot be shown with `map`
  - [ ] `map` GUI
    - Call `map` to toggle either a "Map" view or pane.
    - Cannot be shown with `ls`
  - [ ] `view` GUI
    - Opens a window to either read text or view an image
- Shell
  - [ ] Prettify command outputs
    - [ ] Log printout
  - [ ] chdir multiple directories at once
    - [x] Implement multidir
    - [ ] Check locks for entire path
  - [ ] Add input pre-processing callbacks
- Programs
  - [x] Define an abstract program
    - [ ] Let sub-programs override the GUI
      - Alternatively, add a pane to side (side-by-side view could be cool)
    - [ ] Passphrase unlock for node
  - [ ] Puzzle state editor

- Misc Ideas:
  - Visibility (similar to locks, but for whether nodes can be seen and navigated)
  - Adding files to the path (or smth similar). Global visibility for some files
  - Alias for commands
  - Store programs per-node rather than per-directory
    - If we allow users to move or link directories, then could have puzzles
      requiring files to be moved to certain nodes for programs to see them.
    - Also good for printing.

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

- [x] Add global puzzle state
  - Can be used to solve puzzles (e.g. total explored nodes, was a file opened, etc...)
  - Better to keep information in a "State" object rather than the nodes themselves for 
    debugging puzzles and for interacting with client data vs. server data
- [x] Add global environment variables
  - Semantically different from global state. ENV data is tied to the OS, but 
    puzzle state data is tied to the puzzles.
  - Should store pwd, node history, path, master node, etc...
- [ ] Prettify command outputs
- [ ] Refactor Logging to make clear what it does
- [ ] Show shell and programs in a GUI (so we don't have to switch windows)
- [ ] Start Puzzle state webserver
  - AveryOS backend send puzzle state to webserver.
  - Webserver serves (mobile-friendly) websites to users and forwards user interactions
    back to the AveryOS backend.
- File System
  - [ ] Keep track of whether nodes are visited.
    - Also consider keeping track of whether all of a node's connections are
      visited (both child+parent? or separately?)
- Shell
  - [x] Add `cdid` command to force move to any node by its id
  - [x] Support cd-ing backwards along the node history
  - [ ] Implement cat
    - Maybe allow users to add files to the path
  - [ ] chdir multiple directories at once
  - [ ] Add input pre-processing callbacks
- Programs
  - [x] Define an abstract program
    - [ ] Let sub-programs override the GUI
      - Alternatively, add a pane to side (side-by-side view could be cool)
  - [ ] Make programs a file
    - Or put them in a file
    - Or have nodes keep track of programs separately (**this**)
  - [x] Catch program exceptions
  - [ ] Puzzle state editor
  - [ ] Passphrase unlock for node
    - [x] CLI command version of this program

- Misc Ideas:
  - Visibility (similar to locks, but for whether nodes can be seen and navigated)
  - Adding files to the path (or smth similar). Global visibility for some files
  - Alias for commands
  - Store programs per-node rather than per-directory
    - If we allow users to move or link directories, then could have puzzles
      requiring files to be moved to certain nodes for programs to see them.
    - Also good for printing.

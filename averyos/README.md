# Avery OS

### General coding philosophy

Try to separate the OS design and the puzzle design/solutions. Ideally link
the two using concrete designs/ideas (e.g. locks), or by using callbacks. This
allows the OS to be decoupled from any specific puzzle designs.

**NOTE**: The above goal won't always be possible, but we can try our best.

### Todo

- [x] Separate shell control from entrypoint
  - Better practice, especially if we will move to a server later
- [x] Implement logging to handle and track printouts
  - Also makes it easier to send shell log to user clients
- [x] Add global puzzle state
  - Can be used to solve puzzles (e.g. total explored nodes, was a file opened, etc...)
  - Better to keep information in a "State" object rather than the nodes themselves for 
    debugging puzzles and for interacting with client data vs. server data
- [x] Add callbacks on each node
  - [ ] consider defining event/state objects to pass into callbacks
    - Or have callbacks run entirely off of ENV and puzzle state
  - [x] Callback for entering the node
  - [x] Add locks for accessing nodes
    - For puzzle solving
    - [ ] Put lock checking in find_neighbor
      - Easier for master node to override locks
  - (add other needed callbacks here)
- [ ] Show shell and programs in a GUI (so we don't have to switch windows)
- [ ] Define a "master" node for development
- [ ] Add global environment variables
  - Semantically different from global state. ENV data is tied to the OS, but 
    puzzle state data is tied to the puzzles.
  - Should store pwd, node history, path, master node, etc...
- [ ] Programs
  - [ ] Define an abstract program
    - Make an abstract class which defines a function as the entrypoint
    - Each program is a sub-class which defines it's own entrypoint and keeps track 
      of it's own data.
    - [ ] Let sub-programs override the GUI
      - Alternatively, add a pane to side (side-by-side view could be cool)
  - [ ] Convert non-kernel commands to programs
  - [ ] Puzzle state editor
  - [ ] Passphrase unlock for node
    - [x] CLI command version of this program
- [ ] Puzzle state webserver
  - AveryOS backend send puzzle state to webserver.
  - Webserver serves (mobile-friendly) websites to users and forwards user interactions
    back to the AveryOS backend.

- Misc Ideas:
  - Visibility (similar to locks, but for whether nodes can be seen and navigated)

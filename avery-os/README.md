# Avery OS

### Todo

- [ ] Separate shell control from entrypoint
  - Better practice, especially if we will move to a server later
- [ ] Implement logging to handle and track printouts
  - Also makes it easier to send shell log to user clients
- [ ] Add global/system state
  - Can be used to solve puzzles (e.g. total explored nodes, was a file opened, etc...)
  - Better to keep information in a "State" object rather than the nodes themselves for debugging puzzles and for interacting with client data vs. server data
- [ ] Add locks for accessing nodes
  - For puzzle solving
- [ ] Add users and user states
  - User specific puzzles (e.g. current path length)
  - User's shell instance (logging in and out)
- [ ] Programs
  - [ ] Define an abstract program
    - Make an abstract class which defines a function as the entrypoint
    - Each program is a sub-class which defines it's own entrypoint and keeps track of it's own data.
    - Just CLI programs for now unless we can figure out how to make Python UI/CLI UI programs look the same on python and on the web (this could be a future task).
  - [ ] Global/system state editor
  - [ ] Passphrase unlock for node

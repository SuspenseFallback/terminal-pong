# Terminal pong

Pong made in the terminal.

## Modules used

No external pip modules! The ones imported are:

- threading
- _thread
- time
- curses

## How it works

- Use `curses` to make a wrapper around the main program
- There are 2 parts:
  - The paddle movement
  - The ball movement
 - The paddle is moved in a `while True` loop using `curses` key checking
 - The ball movement is handled in a separate thread

## Physics

Very simple:

- Moving the paddle faster than the y-velocity of the ball increases the y-velocity in that direction
- Otherwise, it stays the same/goes to 0

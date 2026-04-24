# Terminal Wordle — Proposal

## What I'm Building
A terminal-based clone of Wordle. The program picks a random 5-letter word,
and the player has 6 guesses to figure it out. Each guess is scored with
color-coded feedback in the terminal.

## Background
Wordle is the well-known daily word game. After each guess:
- Green = letter is correct and in the right position
- Yellow = letter is in the word but wrong position
- Gray = letter is not in the word

I'm building a version you can play directly in the terminal.

## Plan

### Prototype Milestone
- Load a list of 5-letter words from a text file.
- Pick one at random as the answer.
- Accept guesses from input, check if they match, loop up to 6 times.
- Print plain-text feedback (no colors yet), e.g. "G _ Y _ _".

### Core Milestone
- Add ANSI color codes for green / yellow / gray feedback.
- Validate input: must be exactly 5 letters, must be a real word in the list.
- Show win/lose messages and reveal the answer at the end.
- Track and display which letters have been guessed so far.

### Polish Milestone
- Add a "play again?" loop.
- Track stats across games in the session (games played, win rate, guess
  distribution).
- Clean up code structure, add docstrings, write the README.

## Tech Stack
- Python 3
- Standard library only (no external packages)
- ANSI escape codes for terminal colors

## Deliverables
- `wordle.py` — main game code
- `words.txt` — list of valid 5-letter words
- `README.md` — how to run and play
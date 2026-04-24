# Terminal Wordle

A terminal-based clone of Wordle, written in Python. Guess a hidden 5-letter
word in 6 tries, with color-coded feedback after each guess.

## How to Play
- 🟩 Green: letter is correct and in the right position
- 🟨 Yellow: letter is in the word but wrong position
- ⬜ Gray: letter is not in the word

You have 6 guesses. Guesses must be real 5-letter words from the word list.

## Requirements
- Python 3.8+
- A terminal that supports ANSI colors (most modern terminals do, including
  macOS Terminal, iTerm2, Windows Terminal, and most Linux terminals)

No external packages needed — uses only the standard library.

## How to Run

```
python wordle.py
```

## Sample Session

```
Welcome to Terminal Wordle!
Guess the 5-letter word. You have 6 tries.

Guess 1/6: crane
  C  R [A] N  E
  (A is in the word but in the wrong position)

Guess 2/6: about
  A [B] O  U  T
  (B is correct and in the right position)

...

You won in 4 guesses! The word was ABBEY.

Play again? (y/n):
```

## Files
- `wordle.py` — main game logic
- `words.txt` — list of valid 5-letter answer words
- `README.md` — this file

## Features
- Color-coded feedback using ANSI escape codes
- Input validation (length check + dictionary check)
- Tracks guessed letters across a game
- Session stats: games played, win rate, guess distribution
- Replay loop

## What I Learned
- Handling user input and validation in a game loop
- Using ANSI escape codes for terminal formatting
- Managing game state across multiple rounds
- Structuring a small project into clean functions
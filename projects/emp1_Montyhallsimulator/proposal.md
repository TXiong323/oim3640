# Monty Hall Simulator — Proposal

## What I'm Building
A Python program that simulates the Monty Hall problem thousands of times
to empirically verify whether switching doors really gives a better win rate
than staying.

## Background
The Monty Hall problem is a classic probability puzzle:
- There are 3 doors. Behind one is a car, behind the other two are goats.
- You pick a door.
- The host (who knows what's behind each door) opens one of the other two
  doors to reveal a goat.
- You're asked: do you want to switch to the remaining unopened door, or
  stay with your original choice?

Math says switching wins 2/3 of the time, staying wins 1/3. This project
simulates the game to confirm it.

## Plan

### Prototype Milestone
- Write a function that plays one round of the game with a given strategy
  ("switch" or "stay") and returns whether the player won.
- Run it 100 times for each strategy, print the win rates.

### Core Milestone
- Scale up to 10,000 simulations per strategy.
- Track results in lists for later analysis.
- Print a clean summary comparing the two strategies against theoretical values.

### Polish Milestone
- Add a matplotlib bar chart comparing empirical win rates vs theoretical.
- Add a second chart showing how the win rate converges to the theoretical
  value as the number of simulations grows.
- Clean up code into well-named functions, add docstrings, write the README.

## Tech Stack
- Python 3
- `random` module (standard library)
- `matplotlib` for charts

## Deliverables
- `monty_hall.py` — main simulation code
- `README.md` — how to run it and what the results mean
- Chart images saved as PNG
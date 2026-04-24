# Monty Hall Simulator

A Python simulation of the classic Monty Hall problem. Runs thousands of
games to empirically test whether switching doors beats staying.

## The Problem
Three doors, one car, two goats. You pick a door, the host reveals a goat
behind one of the other two, and asks if you want to switch. Should you?

Probability theory says **yes** — switching wins 2/3 of the time, staying
wins 1/3. This program proves it by simulation.

## Requirements
- Python 3.8+
- matplotlib

Install with:

```
pip install matplotlib
```

## How to Run

```
python monty_hall.py
```

This runs 10,000 simulations for each strategy and prints the results,
then saves two charts as PNG files in the current directory.

## Sample Output

```
Running 10,000 simulations per strategy...

Strategy "stay":    3,341 wins out of 10,000  (33.41%)
Strategy "switch":  6,672 wins out of 10,000  (66.72%)

Theoretical values: stay = 33.33%, switch = 66.67%
```

## Files
- `monty_hall.py` — main simulation script
- `win_rates.png` — bar chart comparing both strategies
- `convergence.png` — line chart showing win rate stabilizing over many trials

## What I Learned
- Using the `random` module to simulate probabilistic events
- Structuring a simulation into reusable functions
- Using matplotlib to turn raw numbers into a clear visual argument
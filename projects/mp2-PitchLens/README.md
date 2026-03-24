# PitchLens

A Python tool that analyzes language patterns in YC startup application essays to uncover 
what writing traits the most compelling pitches share.

## What It Does

- Loads and cleans text from multiple pitch essays
- Counts word frequencies and finds the most common words
- Measures vocabulary richness across essays
- Detects confident vs. hedging language
- Visualizes results with bar charts

## Project Structure
```
PitchLens/
├── data/               # YC essay .txt files go here
├── analysis.py         # Main analysis script
├── PROPOSAL.md
└── README.md
```

## How to Run

1. Add your essay `.txt` files into the `data/` folder
2. Install dependencies:
```
   pip install matplotlib
```
3. Run the analysis:
```
   python analysis.py
```

## Data Sources

Essays collected manually from:
- [r/YCombinator](https://www.reddit.com/r/ycombinator)
- Hacker News "Share your YC application" threads
- Public founder blogs

## What I Found

*(To be updated as analysis progresses)*

## Author

Spark — OIM3640 Spring 2026
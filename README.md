# oim3640

This is my course repository for OIM3640 — Problem Solving with Software at Babson College.

## About Me
- **Name:** Spark Xiong
- **Concentration:** Entrepreneurship
- **Interests:** Playing basketball and video games

## Projects

This repo contains my coursework for OIM3640, organized into three categories:
- **MP** — Mini Projects (required)
- **EMP** — Elective Mini Projects
- **FP** — Final Project

---

### MP1 — Ledger 📒
A command-line expense tracker built with only Python's standard library. Log purchases by category, view formatted tables, search and filter, edit or delete entries, and get weekly/monthly summaries with category breakdowns. All data persists automatically in a CSV file.

📁 [Folder](./projects/mp1-Ledger)

---

### MP2 — PitchLens
A Python text analysis tool that examines the language patterns of 10 real YC startup application essays (Dropbox, VEED, Lago, MagicBell, and others). Measures vocabulary richness and counts confident vs. hedging language to find what writing traits successful pitches share. Outputs visual comparisons via matplotlib.

📁 [Folder](./projects/mp2-PitchLens)

---

### MP3 — SparkFlow
**AI-powered startup opportunity matching for first-time entrepreneurs.** Combines a scenario-based founder assessment with a database of 1,200+ real startup opportunities curated from Reddit, Quora, and Indie Hackers. Uses a three-layer matching pipeline (tag mapping → hard filtering → DeepSeek scoring) to surface the best fit for each user's skills, resources, and risk tolerance. Built with Next.js, Supabase, DeepSeek, and Tavily.

📁 [Folder](./projects/mp3_Sparkflow)  
🔗 **Live:** [sparkflow.ventures](https://sparkflow.ventures)

---

### EMP1 — Monty Hall Simulator
A Python simulation of the classic Monty Hall problem. Runs 10,000 games per strategy to empirically prove that switching doors wins ~2/3 of the time vs. ~1/3 for staying, with matplotlib charts visualizing the result and how empirical win rates converge to theoretical values.

📁 [Folder](./projects/emp1_Montyhallsimulator)

---

### EMP2 — Terminal Wordle
A terminal-based clone of Wordle, written in Python with no external dependencies. Features ANSI color-coded feedback, input validation against a 5-letter word list, an on-screen keyboard tracker that updates after each guess, and session statistics across multiple games.

📁 [Folder](./projects/emp2_Terminalwordle)

---

### FP — Signal 📡
A personal AI/tech daily briefing that runs unattended on GitHub Actions. Pulls candidates from 5 sources (Hacker News, GitHub Trending, YouTube, Product Hunt, Anthropic + OpenAI blogs), deduplicates them against past digests, filters the pool through DeepSeek using my taste profile, and emails me a digest every morning at 7am ET. A longer weekly version runs Sundays. All digests are archived to a public GitHub Pages site for 14 days.

📁 [Folder](./projects/fp_Signal)  
🔗 **Live archive:** [TXiong323.github.io/oim3640](https://TXiong323.github.io/oim3640/)

---

## Other Folders

- **`code/`** — Class demo and review scripts from each lecture session
- **`notebooks/`** — Jupyter notebooks for each chapter of *Think Python*
- **`logs/`** — Weekly learning logs
- **`docs/`** — Auto-generated archive site for the Signal final project (published via GitHub Pages)

## Tech Stack
Across these projects: Python, Flask, Next.js, TypeScript, Tailwind CSS, Jupyter Notebooks, matplotlib, pandas, REST APIs, RSS, GraphQL, Supabase (PostgreSQL), DeepSeek API, Tavily API, GitHub Actions, and Git/GitHub.
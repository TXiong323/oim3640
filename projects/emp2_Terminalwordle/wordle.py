"""Terminal Wordle — a color-coded word-guessing game for the terminal.

Run with:  python wordle.py
"""

from __future__ import annotations

import random
import sys
from pathlib import Path

# ── ANSI color constants ──────────────────────────────────────────────────────

_RESET  = "\033[0m"
_BOLD   = "\033[1m"

# Background colors for guess rows
_BG_GREEN  = "\033[42;30m"   # green bg, black text
_BG_YELLOW = "\033[43;30m"   # amber bg, black text
_BG_GRAY   = "\033[100;37m"  # dark-gray bg, light text

# Foreground colors for the virtual keyboard
_KBD_GREEN  = "\033[1;32m"
_KBD_YELLOW = "\033[1;33m"
_KBD_GRAY   = "\033[90m"
_KBD_NONE   = "\033[97m"     # bright white — unguessed letter

# Score tokens
S_GREEN  = "G"
S_YELLOW = "Y"
S_GRAY   = "X"

MAX_TRIES = 6
KEYBOARD_ROWS = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]


# ── Word loading ──────────────────────────────────────────────────────────────

def load_words(path: str) -> list[str]:
    """Load and return a list of uppercase 5-letter words from *path*.

    Lines that are not exactly 5 alphabetic characters are silently skipped.
    Exits the program if no valid words are found.
    """
    words = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            word = line.strip().upper()
            if len(word) == 5 and word.isalpha():
                words.append(word)
    if not words:
        sys.exit(f"Error: no valid 5-letter words found in {path}")
    return words


# ── Scoring ───────────────────────────────────────────────────────────────────

def score_guess(guess: str, answer: str) -> list[str]:
    """Return a score code for each letter of *guess* compared to *answer*.

    Codes:
      'G' — green  : letter is correct and in the right position
      'Y' — yellow : letter is in the word but in the wrong position
      'X' — gray   : letter is not in the word

    Each answer letter is matched at most once.  Exact matches are resolved
    first so that duplicate letters are handled correctly (e.g. answer APPLE,
    guess PAPER → first P is yellow, second P is green).
    """
    scores = [S_GRAY] * 5
    pool = list(answer)  # tracks which answer letters are still unmatched

    # Pass 1 — exact (green) matches
    for i in range(5):
        if guess[i] == answer[i]:
            scores[i] = S_GREEN
            pool[i] = None  # consume this answer letter

    # Pass 2 — wrong-position (yellow) matches
    for i in range(5):
        if scores[i] == S_GREEN:
            continue
        if guess[i] in pool:
            scores[i] = S_YELLOW
            pool[pool.index(guess[i])] = None  # consume so it can't match twice

    return scores


# ── Board display ─────────────────────────────────────────────────────────────

_SCORE_TO_BG = {S_GREEN: _BG_GREEN, S_YELLOW: _BG_YELLOW, S_GRAY: _BG_GRAY}


def format_row(guess: str, scores: list[str]) -> str:
    """Return one ANSI-colored guess row as a string."""
    cells = [f"{_SCORE_TO_BG[s]} {c} {_RESET}" for c, s in zip(guess, scores)]
    return "  " + " ".join(cells)


def print_board(history: list[tuple[str, list[str]]]) -> None:
    """Print all completed guess rows with a blank line above and below."""
    print()
    for guess, scores in history:
        print(format_row(guess, scores))
    print()


# ── Virtual keyboard ──────────────────────────────────────────────────────────

_STATE_RANK = {None: 0, S_GRAY: 1, S_YELLOW: 2, S_GREEN: 3}
_STATE_COLOR = {
    S_GREEN:  _KBD_GREEN,
    S_YELLOW: _KBD_YELLOW,
    S_GRAY:   _KBD_GRAY,
    None:     _KBD_NONE,
}


def make_keyboard() -> dict[str, str | None]:
    """Return a fresh keyboard-state dict with every letter set to None (unguessed)."""
    return {chr(ord("A") + i): None for i in range(26)}


def update_keyboard(keyboard: dict, guess: str, scores: list[str]) -> None:
    """Upgrade letter states in *keyboard* from the latest guess.

    States only move up the hierarchy (green > yellow > gray); they never
    downgrade.  This means a letter confirmed green stays green even if a
    later guess scores it yellow.
    """
    for letter, score in zip(guess, scores):
        if _STATE_RANK[score] > _STATE_RANK[keyboard[letter]]:
            keyboard[letter] = score


def display_keyboard(keyboard: dict) -> None:
    """Print the QWERTY keyboard with each letter colored by its current state."""
    # Visual row offsets replicate the staggered QWERTY layout
    indents = [0, 1, 3]
    for row, indent in zip(KEYBOARD_ROWS, indents):
        keycaps = "  ".join(
            f"{_STATE_COLOR[keyboard[ch]]}{ch}{_RESET}" for ch in row
        )
        print("  " + " " * indent + keycaps)
    print()


# ── Input validation ──────────────────────────────────────────────────────────

def get_guess(attempt: int, word_set: set[str]) -> str:
    """Prompt the user and return a validated uppercase word.

    Loops until the input is exactly 5 alphabetic characters and appears in
    *word_set*.  Exits cleanly on EOF or keyboard interrupt.
    """
    while True:
        try:
            raw = input(f"  Guess {attempt}/{MAX_TRIES}: ")
        except (EOFError, KeyboardInterrupt):
            print("\n  Goodbye!")
            sys.exit(0)

        word = raw.strip().upper()
        if len(word) != 5:
            print("  ! Must be exactly 5 letters.")
        elif not word.isalpha():
            print("  ! Letters only — no numbers or symbols.")
        elif word not in word_set:
            print(f"  ! '{word}' is not in the word list.")
        else:
            return word


# ── Session statistics ────────────────────────────────────────────────────────

def make_stats() -> dict:
    """Return a fresh session-statistics dict."""
    return {
        "games": 0,
        "wins":  0,
        "distribution": {i: 0 for i in range(1, MAX_TRIES + 1)},
    }


def record_result(stats: dict, won: bool, turns: int) -> None:
    """Update *stats* with the outcome of one completed game."""
    stats["games"] += 1
    if won:
        stats["wins"] += 1
        stats["distribution"][turns] += 1


def display_stats(stats: dict) -> None:
    """Print session totals and a guess-distribution bar chart."""
    games = stats["games"]
    if games == 0:
        return

    wins    = stats["wins"]
    win_pct = 100 * wins / games

    print(f"{_BOLD}-- Session Statistics --{_RESET}")
    print(f"  Games played : {games}")
    print(f"  Wins         : {wins}")
    print(f"  Win rate     : {win_pct:.0f}%")

    if wins:
        dist    = stats["distribution"]
        max_n   = max(dist.values()) or 1
        bar_max = 20
        print(f"\n  Guess distribution:")
        for turn in range(1, MAX_TRIES + 1):
            n      = dist[turn]
            bar_w  = round(bar_max * n / max_n) if n else 0
            bar    = chr(0x2588) * bar_w or chr(0x00B7)   # full block or middle dot
            color  = _KBD_GREEN if (n == max_n and n > 0) else ""
            print(f"    {turn}  {color}{bar}{_RESET}  {n}")

    print()


# ── One game ──────────────────────────────────────────────────────────────────

def play_game(word_list: list[str], word_set: set[str]) -> tuple[bool, int]:
    """Run one complete Wordle game and return (won, number_of_guesses_used)."""
    answer   = random.choice(word_list)
    keyboard = make_keyboard()
    history: list[tuple[str, list[str]]] = []

    print(f"\n  {'─' * 34}")
    print(f"  Guess the 5-letter word — {MAX_TRIES} tries.")
    print(f"  {'─' * 34}")

    for attempt in range(1, MAX_TRIES + 1):
        guess  = get_guess(attempt, word_set)
        scores = score_guess(guess, answer)
        update_keyboard(keyboard, guess, scores)
        history.append((guess, scores))

        print_board(history)
        display_keyboard(keyboard)

        if scores == [S_GREEN] * 5:
            label = "guess" if attempt == 1 else "guesses"
            print(f"  {_KBD_GREEN}{_BOLD}You got it in {attempt} {label}!{_RESET}\n")
            return True, attempt

    print(f"  The word was {_BOLD}{answer}{_RESET}. Better luck next time!\n")
    return False, MAX_TRIES


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    """Load the word list, run the play-again session loop, and show final stats."""
    words_path = Path(__file__).parent / "words.txt"
    word_list  = load_words(str(words_path))
    word_set   = set(word_list)
    stats      = make_stats()

    print(f"\n{_BOLD}+==========================+")
    print(f"|   Terminal Wordle        |")
    print(f"+==========================+{_RESET}")
    print(f"  {_BG_GREEN} G {_RESET} right letter, right place")
    print(f"  {_BG_YELLOW} Y {_RESET} right letter, wrong place")
    print(f"  {_BG_GRAY} X {_RESET} letter not in word")

    while True:
        won, turns = play_game(word_list, word_set)
        record_result(stats, won, turns)
        display_stats(stats)

        try:
            again = input("  Play again? (y/n): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            break
        if again not in ("y", "yes"):
            break

    print(f"\n{_BOLD}  Thanks for playing!{_RESET}\n")


def demo_colors() -> None:
    """Print a color-verification strip and exit.

    Run with:  python wordle.py --demo
    """
    # HAPPY scored as: H=gray  A=yellow  P=green  P=yellow  Y=gray
    guess  = "HAPPY"
    scores = [S_GRAY, S_YELLOW, S_GREEN, S_YELLOW, S_GRAY]

    print(f"\n{_BOLD}Color verification — HAPPY{_RESET}")
    print(format_row(guess, scores))
    print()

    kb = make_keyboard()
    update_keyboard(kb, guess, scores)
    display_keyboard(kb)

    print(f"  {_BG_GREEN} G {_RESET} green  |  {_BG_YELLOW} Y {_RESET} yellow  |  {_BG_GRAY} X {_RESET} gray\n")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo_colors()
    else:
        main()

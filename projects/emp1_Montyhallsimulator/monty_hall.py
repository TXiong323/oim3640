"""Monty Hall Problem Simulator

Simulates the classic three-door game thousands of times to empirically
verify that switching wins ~2/3 of the time and staying wins ~1/3.
"""

import random
import matplotlib.pyplot as plt


# ── Prototype ─────────────────────────────────────────────────────────────────

def play_round(strategy: str) -> bool:
    """Play one round of the Monty Hall game and return True if the player wins.

    Args:
        strategy: "switch" to switch doors after the host reveals a goat,
                  "stay" to keep the original choice.
    """
    doors = [0, 1, 2]
    car = random.choice(doors)
    pick = random.choice(doors)

    # Host opens a door that is neither the player's pick nor the car.
    goat_doors = [d for d in doors if d != pick and d != car]
    host_opens = random.choice(goat_doors)

    if strategy == "switch":
        remaining = [d for d in doors if d != pick and d != host_opens]
        final = remaining[0]
    else:
        final = pick

    return final == car


# ── Core ──────────────────────────────────────────────────────────────────────

def run_simulations(strategy: str, n: int = 10_000) -> list[bool]:
    """Run n rounds of the Monty Hall game for a given strategy.

    Args:
        strategy: "switch" or "stay".
        n:        Number of rounds to simulate.

    Returns:
        List of bool outcomes (True = win).
    """
    return [play_round(strategy) for _ in range(n)]


def print_summary(results: dict[str, list[bool]], n: int) -> None:
    """Print a formatted summary comparing both strategies to theoretical values.

    Args:
        results: Mapping of strategy name to list of outcomes.
        n:       Number of simulations run per strategy.
    """
    theoretical = {"stay": 1 / 3, "switch": 2 / 3}
    print(f"\nRunning {n:,} simulations per strategy...\n")
    for strategy, outcomes in results.items():
        wins = sum(outcomes)
        pct = wins / n * 100
        theory = theoretical[strategy] * 100
        print(
            f'Strategy "{strategy:6}": {wins:,} wins out of {n:,}'
            f"  ({pct:.2f}%)  [theory {theory:.2f}%]"
        )
    print()


# ── Polish ────────────────────────────────────────────────────────────────────

def plot_win_rates(results: dict[str, list[bool]], n: int, path: str = "win_rates.png") -> None:
    """Save a bar chart comparing empirical win rates vs theoretical values.

    Args:
        results: Mapping of strategy name to list of outcomes.
        n:       Number of simulations per strategy.
        path:    Output file path.
    """
    strategies = list(results.keys())
    empirical = [sum(results[s]) / n * 100 for s in strategies]
    theoretical = [1 / 3 * 100, 2 / 3 * 100]

    x = range(len(strategies))
    width = 0.35

    fig, ax = plt.subplots(figsize=(7, 5))
    bars_emp = ax.bar([i - width / 2 for i in x], empirical, width,
                      label="Empirical", color=["#4C72B0", "#4C72B0"], alpha=0.85)
    bars_the = ax.bar([i + width / 2 for i in x], theoretical, width,
                      label="Theoretical", color=["#DD8452", "#DD8452"], alpha=0.85)

    ax.set_ylabel("Win Rate (%)")
    ax.set_title(f"Monty Hall Win Rates ({n:,} simulations)")
    ax.set_xticks(list(x))
    ax.set_xticklabels([s.capitalize() for s in strategies])
    ax.set_ylim(0, 90)
    ax.legend()
    ax.axhline(100 / 3, color="gray", linestyle="--", linewidth=0.8)
    ax.axhline(200 / 3, color="gray", linestyle="--", linewidth=0.8)

    for bar in list(bars_emp) + list(bars_the):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1,
            f"{bar.get_height():.1f}%",
            ha="center", va="bottom", fontsize=9,
        )

    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"Saved: {path}")


def plot_convergence(results: dict[str, list[bool]], path: str = "convergence.png") -> None:
    """Save a line chart showing how each strategy's win rate converges over trials.

    Args:
        results: Mapping of strategy name to list of outcomes.
        path:    Output file path.
    """
    fig, ax = plt.subplots(figsize=(9, 5))

    colors = {"stay": "#4C72B0", "switch": "#DD8452"}
    theory = {"stay": 1 / 3, "switch": 2 / 3}

    for strategy, outcomes in results.items():
        n = len(outcomes)
        # Cumulative win rate at each trial index
        running = [sum(outcomes[: i + 1]) / (i + 1) * 100 for i in range(n)]
        ax.plot(range(1, n + 1), running, label=f"{strategy.capitalize()} (empirical)",
                color=colors[strategy], linewidth=1, alpha=0.8)
        ax.axhline(theory[strategy] * 100, color=colors[strategy],
                   linestyle="--", linewidth=1.2, label=f"{strategy.capitalize()} (theory {theory[strategy]*100:.1f}%)")

    ax.set_xlabel("Number of Simulations")
    ax.set_ylabel("Win Rate (%)")
    ax.set_title("Win Rate Convergence to Theoretical Values")
    ax.legend(loc="right")
    ax.set_ylim(0, 100)

    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"Saved: {path}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    """Run the full Monty Hall simulation and produce summary + charts."""
    N = 10_000
    random.seed(42)

    results = {
        "stay": run_simulations("stay", N),
        "switch": run_simulations("switch", N),
    }

    print_summary(results, N)
    plot_win_rates(results, N)
    plot_convergence(results)


if __name__ == "__main__":
    main()

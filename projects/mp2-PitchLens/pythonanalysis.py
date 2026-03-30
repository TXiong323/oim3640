import os
import string
import matplotlib.pyplot as plt

# --------------------------------------------------------
# STOP WORDS
# --------------------------------------------------------
STOP_WORDS = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to",
    "for", "of", "with", "is", "are", "was", "were", "be", "been",
    "it", "its", "this", "that", "we", "our", "they", "their", "you",
    "your", "i", "my", "me", "he", "she", "his", "her", "as", "by",
    "not", "so", "if", "from", "up", "out", "also", "have", "has",
    "had", "do", "does", "will", "would", "can", "could", "than",
    "more", "about", "all", "what", "who", "how", "which", "when",
    "there", "their", "them", "us", "any", "no", "into", "than",
    "well", "been", "just", "very", "each", "both", "only", "most"
}

# --------------------------------------------------------
# CONFIDENCE vs HEDGING word lists
# --------------------------------------------------------
CONFIDENT_WORDS = {
    "will", "built", "launched", "proven", "achieved", "delivered",
    "demonstrated", "completed", "secured", "established", "committed",
    "growing", "winning", "leading", "generated", "raised", "closed"
}

HEDGING_WORDS = {
    "might", "maybe", "perhaps", "hope", "trying", "possibly",
    "potentially", "likely", "uncertain", "unclear", "attempt",
    "consider", "believe", "think", "expect", "planning", "intend"
}

# --------------------------------------------------------
# Build data folder path relative to this script
# --------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(SCRIPT_DIR, "data")


# --------------------------------------------------------
# STEP 1: Load text
# --------------------------------------------------------
def load_text(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


# --------------------------------------------------------
# STEP 2: Clean text
# --------------------------------------------------------
def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text


# --------------------------------------------------------
# STEP 3: Count word frequencies (excluding stop words)
# --------------------------------------------------------
def count_words(text):
    words = text.split()
    frequency = {}
    for word in words:
        if word not in STOP_WORDS and len(word) > 1:
            frequency[word] = frequency.get(word, 0) + 1
    return frequency


# --------------------------------------------------------
# STEP 4: Top N words
# --------------------------------------------------------
def top_n_words(frequency, n=10):
    sorted_words = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
    return sorted_words[:n]


# --------------------------------------------------------
# STEP 5: Basic stats
# --------------------------------------------------------
def print_stats(filename, raw_text, frequency):
    total_words = len(raw_text.split())
    unique_words = len(frequency)
    top_words = top_n_words(frequency, 10)

    print("=" * 45)
    print(f"Essay: {filename}")
    print("=" * 45)
    print(f"Total words:  {total_words}")
    print(f"Unique words: {unique_words}")
    print(f"\nTop 10 most common words:")
    for i, (word, count) in enumerate(top_words, 1):
        print(f"  {i:2}. {word:<20} {count}")
    print()


# --------------------------------------------------------
# QUESTION 1: Vocabulary richness (unique / total words)
# --------------------------------------------------------
def vocabulary_richness(raw_text, frequency):
    total_words = len(raw_text.split())
    unique_words = len(frequency)
    return round(unique_words / total_words, 3)


def print_vocabulary_ranking(results):
    print("\n========================================")
    print("   Q1: Vocabulary Richness Ranking")
    print("   (unique words / total words)")
    print("========================================")
    ranked = sorted(results, key=lambda x: x["richness"], reverse=True)
    for i, r in enumerate(ranked, 1):
        name = r["name"].replace(".txt", "")
        print(f"  {i:2}. {name:<20} {r['richness']}")


# --------------------------------------------------------
# QUESTION 2: Confidence score (confident - hedging words)
# --------------------------------------------------------
def confidence_score(raw_text):
    words = raw_text.lower().split()
    confident_count = sum(1 for w in words if w in CONFIDENT_WORDS)
    hedging_count = sum(1 for w in words if w in HEDGING_WORDS)
    score = confident_count - hedging_count
    return confident_count, hedging_count, score


def print_confidence_ranking(results):
    print("\n========================================")
    print("   Q2: Confidence vs Hedging Language")
    print("   (confident words - hedging words)")
    print("========================================")
    print(f"  {'Essay':<22} {'Confident':>10} {'Hedging':>8} {'Score':>7}")
    print("  " + "-" * 50)
    ranked = sorted(results, key=lambda x: x["conf_score"], reverse=True)
    for r in ranked:
        name = r["name"].replace(".txt", "")
        print(f"  {name:<22} {r['conf_count']:>10} {r['hedge_count']:>8} {r['conf_score']:>7}")


# --------------------------------------------------------
# CHART 1: Vocabulary richness bar chart
# --------------------------------------------------------
def plot_vocabulary_richness(results):
    ranked = sorted(results, key=lambda x: x["richness"], reverse=True)
    names = [r["name"].replace(".txt", "") for r in ranked]
    scores = [r["richness"] for r in ranked]

    plt.figure(figsize=(12, 6))
    bars = plt.bar(names, scores, color="steelblue", edgecolor="white")

    for bar, score in zip(bars, scores):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.003,
            str(score),
            ha="center", va="bottom", fontsize=9
        )

    plt.title("PitchLens: Vocabulary Richness by Essay", fontsize=14, fontweight="bold")
    plt.xlabel("Startup Essay", fontsize=11)
    plt.ylabel("Richness Score (unique / total words)", fontsize=11)
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(SCRIPT_DIR, "vocabulary_richness.png"), dpi=150)
    plt.show()
    print("  Chart 1 saved as vocabulary_richness.png")


# --------------------------------------------------------
# CHART 2: Confidence vs Hedging grouped bar chart
# --------------------------------------------------------
def plot_confidence_scores(results):
    ranked = sorted(results, key=lambda x: x["conf_score"], reverse=True)
    names = [r["name"].replace(".txt", "") for r in ranked]
    confident = [r["conf_count"] for r in ranked]
    hedging = [r["hedge_count"] for r in ranked]

    x = range(len(names))
    width = 0.35

    fig, ax = plt.subplots(figsize=(12, 6))
    bars1 = ax.bar([i - width / 2 for i in x], confident, width,
                   label="Confident words", color="seagreen", edgecolor="white")
    bars2 = ax.bar([i + width / 2 for i in x], hedging, width,
                   label="Hedging words", color="tomato", edgecolor="white")

    # Value labels
    for bar in bars1:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                str(int(bar.get_height())), ha="center", va="bottom", fontsize=9)
    for bar in bars2:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                str(int(bar.get_height())), ha="center", va="bottom", fontsize=9)

    ax.set_title("PitchLens: Confident vs Hedging Language by Essay",
                 fontsize=14, fontweight="bold")
    ax.set_xlabel("Startup Essay", fontsize=11)
    ax.set_ylabel("Word Count", fontsize=11)
    ax.set_xticks(list(x))
    ax.set_xticklabels(names, rotation=30, ha="right")
    ax.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(SCRIPT_DIR, "confidence_scores.png"), dpi=150)
    plt.show()
    print("  Chart 2 saved as confidence_scores.png")


# --------------------------------------------------------
# MAIN
# --------------------------------------------------------
def main():
    print("\n========================================")
    print("       PitchLens - Text Analysis        ")
    print("========================================\n")

    if not os.path.exists(DATA_FOLDER):
        print(f"ERROR: Could not find data folder at: {DATA_FOLDER}")
        return

    results = []

    for filename in sorted(os.listdir(DATA_FOLDER)):
        if filename.endswith(".txt"):
            filepath = os.path.join(DATA_FOLDER, filename)
            raw_text = load_text(filepath)
            cleaned = clean_text(raw_text)
            frequency = count_words(cleaned)

            print_stats(filename, raw_text, frequency)

            richness = vocabulary_richness(raw_text, frequency)
            conf_count, hedge_count, conf_score = confidence_score(raw_text)

            results.append({
                "name": filename,
                "richness": richness,
                "conf_count": conf_count,
                "hedge_count": hedge_count,
                "conf_score": conf_score,
            })

    print_vocabulary_ranking(results)
    print_confidence_ranking(results)

    print("\n========================================")
    print("   Generating Charts...")
    print("========================================")
    plot_vocabulary_richness(results)
    plot_confidence_scores(results)


if __name__ == "__main__":
    main()
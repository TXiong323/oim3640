import os
import string

# --------------------------------------------------------
# STOP WORDS - common words we want to ignore
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
# Build data folder path relative to this script's location
# --------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(SCRIPT_DIR, "data")


# --------------------------------------------------------
# STEP 1: Load text from a .txt file
# --------------------------------------------------------
def load_text(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


# --------------------------------------------------------
# STEP 2: Clean the text
# --------------------------------------------------------
def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text


# --------------------------------------------------------
# STEP 3: Count word frequencies
# --------------------------------------------------------
def count_words(text):
    words = text.split()
    frequency = {}
    for word in words:
        if word not in STOP_WORDS and len(word) > 1:
            frequency[word] = frequency.get(word, 0) + 1
    return frequency


# --------------------------------------------------------
# STEP 4: Get top N words
# --------------------------------------------------------
def top_n_words(frequency, n=10):
    sorted_words = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
    return sorted_words[:n]


# --------------------------------------------------------
# STEP 5: Print stats for one essay
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
# MAIN - Run analysis on all essays in data/
# --------------------------------------------------------
def main():
    print("\n========================================")
    print("       PitchLens - Text Analysis        ")
    print("========================================\n")

    # Check if data folder exists
    if not os.path.exists(DATA_FOLDER):
        print(f"ERROR: Could not find data folder at: {DATA_FOLDER}")
        return

    files_found = 0
    for filename in sorted(os.listdir(DATA_FOLDER)):
        if filename.endswith(".txt"):
            files_found += 1
            filepath = os.path.join(DATA_FOLDER, filename)
            raw_text = load_text(filepath)
            cleaned = clean_text(raw_text)
            frequency = count_words(cleaned)
            print_stats(filename, raw_text, frequency)

    if files_found == 0:
        print("No .txt files found in the data/ folder.")


if __name__ == "__main__":
    main()
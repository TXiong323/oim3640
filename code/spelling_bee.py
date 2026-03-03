"""
NYT Spelling Bee Solver
-----------------------
Finds all valid words from a word list given:
  - A set of 7 allowed letters
  - A required center letter
  - Words must be at least 4 letters long
  - Words can only use the allowed letters (letters can repeat)
  - Every word must contain the center letter

Usage:
    python spelling_bee.py
"""


def load_words(filepath):
    """Load words from a text file (one word per line)."""
    with open(filepath, "r") as f:
        words = [line.strip().lower() for line in f if line.strip()]
    return words


def is_valid(word, allowed_letters, center_letter):
    """Check if a word is a valid Spelling Bee answer."""
    # Must be at least 4 letters
    if len(word) < 4:
        return False

    # Must contain the center letter
    if center_letter not in word:
        return False

    # Every letter in the word must be in the allowed set
    if not all(ch in allowed_letters for ch in word):
        return False

    return True


def is_pangram(word, allowed_letters):
    """Check if a word uses ALL 7 allowed letters."""
    return all(letter in word for letter in allowed_letters)


def score_word(word, allowed_letters):
    """Calculate the point value of a word."""
    if len(word) == 4:
        points = 1
    else:
        points = len(word)

    # Pangrams get 7 bonus points
    if is_pangram(word, allowed_letters):
        points += 7

    return points


def solve(words, allowed_letters, center_letter):
    """Find all valid Spelling Bee words and return them sorted."""
    allowed_set = set(allowed_letters)
    valid_words = []

    for word in words:
        if is_valid(word, allowed_set, center_letter):
            valid_words.append(word)

    # Sort alphabetically
    valid_words.sort()
    return valid_words


def display_results(valid_words, allowed_letters):
    """Print the results in a readable format."""
    pangrams = [w for w in valid_words if is_pangram(w, allowed_letters)]
    total_score = sum(score_word(w, allowed_letters) for w in valid_words)

    print(f"\n{'='*50}")
    print(f"  Found {len(valid_words)} words | Total score: {total_score} pts")
    print(f"{'='*50}")

    if pangrams:
        print(f"\n⭐ PANGRAMS ({len(pangrams)}):")
        for word in pangrams:
            print(f"   {word.upper()} (+{score_word(word, allowed_letters)} pts)")

    print(f"\nAll words by length:")
    # Group by length
    by_length = {}
    for word in valid_words:
        length = len(word)
        if length not in by_length:
            by_length[length] = []
        by_length[length].append(word)

    for length in sorted(by_length.keys()):
        group = by_length[length]
        print(f"\n  {length} letters ({len(group)} words):")
        # Print in rows of 5
        for i in range(0, len(group), 5):
            row = group[i:i+5]
            print(f"    {', '.join(row)}")


def get_letters_from_user():
    """Prompt the user for today's letters."""
    print("NYT Spelling Bee Solver")
    print("-" * 30)

    letters_input = input("Enter all 7 letters (e.g. abceklo): ").strip().lower()
    if len(letters_input) != 7:
        print("Error: Please enter exactly 7 letters.")
        return None, None

    center = input("Enter the CENTER letter: ").strip().lower()
    if len(center) != 1 or center not in letters_input:
        print("Error: Center letter must be one of the 7 letters.")
        return None, None

    return list(letters_input), center


def main():
    # Get today's letters from the user
    allowed_letters, center_letter = get_letters_from_user()
    if allowed_letters is None:
        return

    print(f"\nLetters: {' '.join(l.upper() for l in allowed_letters)}")
    print(f"Center:  {center_letter.upper()}")

    # Load the word list
    # Try multiple common paths for words.txt
    possible_paths = [
        "../data/words.txt",    # from code/ folder (per class instructions)
        "data/words.txt",       # from project root
        "words.txt",            # same directory
        "/usr/share/dict/words" # system dictionary (fallback)
    ]

    words = None
    for path in possible_paths:
        try:
            words = load_words(path)
            print(f"Loaded {len(words)} words from: {path}")
            break
        except FileNotFoundError:
            continue

    if words is None:
        print("Error: Could not find words.txt. Tried:")
        for p in possible_paths:
            print(f"  - {p}")
        return

    # Solve and display
    valid_words = solve(words, allowed_letters, center_letter)
    display_results(valid_words, allowed_letters)


if __name__ == "__main__":
    main()
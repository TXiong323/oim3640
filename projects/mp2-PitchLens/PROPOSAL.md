## My Project Proposal

**Project Name:** PitchLens

**What I'm building:** A Python-based text analysis tool that compares language patterns 
across real YC startup application essays to uncover what writing traits — confidence, 
vocabulary richness, specificity — the most compelling pitches tend to share.

**Why I chose this:** I'm interested in entrepreneurship and want to understand what 
language and framing make a startup pitch compelling. Rather than just reading advice 
about pitching, I want to find data-backed patterns directly from real essays — insights 
I can apply to my own ideas and projects.

**Core features:**
- Load and clean text from multiple YC pitch essays stored as `.txt` files
- Count word frequencies and identify the most common words per essay
- Measure vocabulary richness (unique word ratio) across essays to compare writing depth
- Detect "confidence language" (e.g., "will", "proven", "launched", "built") vs. hedging 
  words (e.g., "might", "maybe", "hope", "trying") and compute a confidence score
- Visualize findings with bar charts comparing vocabulary richness and confidence scores 
  across essays

**Data source:**
- 5–10 publicly available YC application essays collected manually from Reddit 
  (r/YCombinator), Hacker News "Share your YC application" threads, and founder blogs
- Stored locally as plain `.txt` files in a `data/` folder

**Tech stack:**
- Python 3
- `collections.Counter` for word frequency
- `matplotlib` for visualizations
- `string` and basic regex for text cleaning
- No external APIs required for core features

**Stretch goals (if time allows):**
- Add sentiment analysis using `TextBlob`
- Compare essays from funded vs. unfunded applicants if enough data is available
- Generate a summary report as a `.txt` or `.csv` output file

**What I don't know yet:**
- How to reliably find enough public YC essays in plain text format
- How to best measure "confidence" in language quantitatively (simple word list vs. 
  weighted scoring)
- Whether stop-word removal will meaningfully change the results
- How consistent the essay formats are across different founders and years
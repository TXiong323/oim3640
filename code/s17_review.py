"""
Session 17 Review (3/26)
Topic: Ch 12 Text Analysis

Your Turn: Read a book from Project Gutenberg and do text analysis.
- Count word frequencies (counting pattern)
- Find unique words (set)
- Sort by frequency (list of tuples)
- Find words that appear exactly once
Use only built-in Python - no external libraries yet!
"""

import unicodedata


# ---------- Read words from a file ----------

filename = 'dr_jekyll.txt'

words = []
for line in open(filename):
    for word in line.split():
        words.append(word.strip().lower())

print(len(words))         # total words
print(len(set(words)))    # unique words (set!)


# ---------- Handle dashes and punctuation ----------

def split_line(line):
    # replace the em-dash with a space, then split
    return line.replace('—', ' ').split()


# build a list of punctuation marks that appear in the book
punc_marks = {}
for line in open(filename):
    for char in line:
        category = unicodedata.category(char)
        if category.startswith('P'):
            punc_marks[char] = 1

punctuation = ''.join(punc_marks)
print(punctuation)


def clean_word(word):
    return word.strip(punctuation).lower()


# ---------- Count unique words (cleaner version) ----------

unique_words = {}
for line in open(filename):
    for word in split_line(line):
        word = clean_word(word)
        unique_words[word] = 1

print(len(unique_words))
print(sorted(unique_words, key=len)[-5:])   # 5 longest words


# ---------- Word frequencies (counting pattern) ----------

word_counter = {}
for line in open(filename):
    for word in split_line(line):
        word = clean_word(word)
        if word not in word_counter:
            word_counter[word] = 1
        else:
            word_counter[word] += 1


# ---------- Sort by frequency ----------

def second_element(t):
    return t[1]


items = sorted(word_counter.items(), key=second_element, reverse=True)
for word, freq in items[:5]:
    print(freq, word, sep='\t')


# ---------- Optional parameter (num=5 by default) ----------

def print_most_common(word_counter, num=5):
    items = sorted(word_counter.items(), key=second_element, reverse=True)
    for word, freq in items[:num]:
        print(freq, word, sep='\t')


print_most_common(word_counter)       # uses default num=5
print_most_common(word_counter, 3)    # override to 3


# ---------- Dictionary subtraction (spell check idea) ----------

word_list = open('words.txt').read().split()
valid_words = {}
for word in word_list:
    valid_words[word] = 1


def subtract(d1, d2):
    res = {}
    for key in d1:
        if key not in d2:
            res[key] = d1[key]
    return res


diff = subtract(word_counter, valid_words)
print_most_common(diff)


# ---------- Find words that appear exactly once ----------

singletons = []
for word, freq in diff.items():
    if freq == 1:
        singletons.append(word)

print(singletons[-5:])


# ---------- Random words ----------

import random

words_list = list(word_counter)
weights = word_counter.values()

# random words without weights
for i in range(6):
    word = random.choice(words_list)
    print(word, end=' ')
print()

# random words with weights (frequency-based)
random_words = random.choices(words_list, weights=weights, k=6)
print(' '.join(random_words))


# ---------- Bigrams ----------

bigram_counter = {}


def count_bigram(bigram):
    key = tuple(bigram)
    if key not in bigram_counter:
        bigram_counter[key] = 1
    else:
        bigram_counter[key] += 1


window = []


def process_word(word):
    window.append(word)
    if len(window) == 2:
        count_bigram(window)
        window.pop(0)


for line in open(filename):
    for word in split_line(line):
        word = clean_word(word)
        process_word(word)

print_most_common(bigram_counter)


# ---------- Markov chain text generation ----------

successor_map = {}


def add_bigram(bigram):
    first, second = bigram
    if first not in successor_map:
        successor_map[first] = [second]
    else:
        successor_map[first].append(second)


window = []


def process_word_bigram(word):
    window.append(word)
    if len(window) == 2:
        add_bigram(window)
        window.pop(0)


for line in open(filename):
    for word in split_line(line):
        word = clean_word(word)
        process_word_bigram(word)


# generate a sequence of random words using the successor map
word = 'although'
for i in range(10):
    successors = successor_map[word]
    word = random.choice(successors)
    print(word, end=' ')
print()
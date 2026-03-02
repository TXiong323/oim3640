# OIM3640 - 2026 Spring

(oim3640/projects/<mp1_Ledger>/)

# Ledger 📒

A command-line expense tracker to log your purchases, organize them by category, and review your spending patterns over time. Data saves automatically so nothing is lost between sessions.

---

## What It Does

- Log expenses with item name, price, and category
- View all expenses in a formatted table
- Edit or delete existing expenses
- Search expenses by keyword
- Filter expenses by category
- See weekly and monthly spending summaries with category breakdowns
- All data persists in a CSV file — your expenses are saved automatically

---

## How to Run

Make sure you have Python 3 installed. Then run:

```bash
python3 ledger.py
```

No external libraries needed — Ledger uses only Python's built-in `csv`, `os`, and `datetime` modules.

---

## How to Use

1. Run the program and pick an option from the menu (1–9)
2. To add an expense: enter the item name, price, and choose a category
3. To view, search, filter, edit, or delete: follow the on-screen prompts
4. To see summaries: pick weekly or monthly to see spending by category
5. Type `9` to quit — your data is already saved

---

## Example

```
Welcome to Ledger!
  Loaded 2 saved expense(s).

========= LEDGER =========
  1. Add expense
  2. View all expenses
  3. Delete expense
  4. Edit expense
  5. Search expenses
  6. Filter by category
  7. Weekly summary
  8. Monthly summary
  9. Quit
==========================
  Choose an option: 1

--- Add Expense (type 'done' to stop) ---
  Item name: Groceries
  Price: $45.00
  Categories:
    1. Food
    2. Transport
    3. Entertainment
    4. Shopping
    5. Bills
    6. Health
    7. Education
    8. Other
  Pick a number (or press Enter for 'Other'): 1
  Added: Groceries — $45.00 [Food] on 2026-03-01

  Item name: done

  Choose an option: 8

  === Monthly Summary (2026-03) ===
  Food            $   45.00  ( 62.1%)  ############
  Transport       $   27.50  ( 37.9%)  #######

  Total this month: $72.50  (3 purchases)
  Daily average:   $72.50
```

---

## File Structure

```
mp1_Ledger/
├── ledger.py          # Main program
├── ledger_data.csv    # Auto-generated data file (created on first use)
├── PROPOSAL.md        # Project proposal
└── README.md          # This file
```

---

## Categories

Ledger includes 8 built-in categories: Food, Transport, Entertainment, Shopping, Bills, Health, Education, and Other.

---

## Author

Built as part of Mini Project 1.
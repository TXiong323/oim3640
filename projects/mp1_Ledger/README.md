# OIM3640 - 2026 Spring

(oim3640/projects/<mp1_Ledger>/)

# Ledger 📒

A simple command-line account book to log your purchases and keep track of your spending.

---

## What It Does

- Log an expense by entering an item name and price
- View all your logged expenses in a clean list
- See your total spending at a glance

---

## How to Run

Make sure you have Python 3 installed. Then run:

```bash
python3 account_book.py
```

---

## How to Use

1. When prompted, type in what you bought
2. Enter the price
3. Keep adding items as needed
4. Type `done` when you're finished
5. Ledger will print a summary of everything you spent

---

## Example

```
=== Account Book ===
Log your expenses below.
Type 'done' when you're finished.

What did you buy? (or type 'done' to finish): Groceries
How much did 'Groceries' cost? $45.00
✓ Added 'Groceries' for $45.00

What did you buy? (or type 'done' to finish): Coffee
How much did 'Coffee' cost? $4.80
✓ Added 'Coffee' for $4.80

What did you buy? (or type 'done' to finish): done

--- Your Expenses ---
  Groceries: $45.00
  Coffee: $4.80
---------------------
  Total: $49.80
```

---

## Requirements

- Python 3 (no external libraries needed)

---

## Author

Built as part of Mini Project 1.
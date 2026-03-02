"""
LEDGER - Personal Expense Tracker
A command-line tool for logging purchases and reviewing spending patterns.

Features:
  - Log expenses with item name, price, category, and automatic date
  - Save/load data to CSV file (persistent across sessions)
  - View all expenses or filter by category
  - Weekly and monthly spending summaries
  - Delete expenses
  - Search expenses by keyword
  - Edit existing expenses
"""

import csv
import os
from datetime import datetime, timedelta


# ============================================================
# FILE PERSISTENCE
# ============================================================

DATA_FILE = "ledger_data.csv"
FIELDNAMES = ["id", "date", "item", "price", "category"]

CATEGORIES = [
    "Food",
    "Transport",
    "Entertainment",
    "Shopping",
    "Bills",
    "Health",
    "Education",
    "Other",
]


def load_expenses():
    """Load expenses from CSV file. Returns a list of dicts."""
    expenses = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                row["price"] = float(row["price"])
                row["id"] = int(row["id"])
                expenses.append(row)
    return expenses


def save_expenses(expenses):
    """Save all expenses to CSV file."""
    with open(DATA_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(expenses)


def next_id(expenses):
    """Get the next available ID number."""
    if not expenses:
        return 1
    return max(e["id"] for e in expenses) + 1


# ============================================================
# INPUT HELPERS
# ============================================================

def get_price():
    """Prompt for a valid price. Returns a float or None to cancel."""
    while True:
        raw = input("  Price: $").strip()
        if raw.lower() == "cancel":
            return None
        try:
            price = float(raw)
            if price <= 0:
                print("  Price must be positive. Try again.")
                continue
            return round(price, 2)
        except ValueError:
            print("  That's not a valid number. Try again (or type 'cancel').")


def get_category():
    """Prompt user to pick a category. Returns the category string."""
    print("  Categories:")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"    {i}. {cat}")
    while True:
        choice = input("  Pick a number (or press Enter for 'Other'): ").strip()
        if choice == "":
            return "Other"
        try:
            idx = int(choice)
            if 1 <= idx <= len(CATEGORIES):
                return CATEGORIES[idx - 1]
            print(f"  Please pick 1–{len(CATEGORIES)}.")
        except ValueError:
            print("  Enter a number.")


# ============================================================
# CORE ACTIONS
# ============================================================

def add_expense(expenses):
    """Add one or more expenses interactively."""
    print("\n--- Add Expense (type 'done' to stop) ---")
    while True:
        name = input("  Item name: ").strip()
        if name.lower() == "done":
            break
        if not name:
            print("  Item name can't be empty.")
            continue

        price = get_price()
        if price is None:
            continue

        category = get_category()
        today = datetime.now().strftime("%Y-%m-%d")

        expense = {
            "id": next_id(expenses),
            "date": today,
            "item": name,
            "price": price,
            "category": category,
        }
        expenses.append(expense)
        save_expenses(expenses)
        print(f"  Added: {name} — ${price:.2f} [{category}] on {today}\n")


def show_expenses(expenses):
    """Display all expenses in a formatted table."""
    if not expenses:
        print("\n  No expenses recorded yet.")
        return

    print(f"\n  {'ID':<5} {'Date':<12} {'Item':<25} {'Category':<15} {'Price':>8}")
    print("  " + "-" * 67)
    total = 0
    for e in expenses:
        print(f"  {e['id']:<5} {e['date']:<12} {e['item']:<25} {e['category']:<15} ${e['price']:>7.2f}")
        total += e["price"]
    print("  " + "-" * 67)
    print(f"  {'TOTAL':<58} ${total:>7.2f}")
    print(f"  {len(expenses)} expense(s)\n")


def delete_expense(expenses):
    """Delete an expense by its ID."""
    if not expenses:
        print("\n  Nothing to delete.")
        return

    show_expenses(expenses)
    raw = input("  Enter the ID to delete (or 'cancel'): ").strip()
    if raw.lower() == "cancel":
        return

    try:
        target_id = int(raw)
    except ValueError:
        print("  Invalid ID.")
        return

    for i, e in enumerate(expenses):
        if e["id"] == target_id:
            removed = expenses.pop(i)
            save_expenses(expenses)
            print(f"  Deleted: {removed['item']} — ${removed['price']:.2f}")
            return

    print(f"  No expense with ID {target_id} found.")


def edit_expense(expenses):
    """Edit an existing expense."""
    if not expenses:
        print("\n  Nothing to edit.")
        return

    show_expenses(expenses)
    raw = input("  Enter the ID to edit (or 'cancel'): ").strip()
    if raw.lower() == "cancel":
        return

    try:
        target_id = int(raw)
    except ValueError:
        print("  Invalid ID.")
        return

    target = None
    for e in expenses:
        if e["id"] == target_id:
            target = e
            break

    if target is None:
        print(f"  No expense with ID {target_id} found.")
        return

    print(f"\n  Editing: {target['item']} — ${target['price']:.2f} [{target['category']}]")
    print("  (Press Enter to keep current value)\n")

    new_name = input(f"  Item name [{target['item']}]: ").strip()
    if new_name:
        target["item"] = new_name

    new_price = input(f"  Price [${target['price']:.2f}]: ").strip()
    if new_price:
        try:
            target["price"] = round(float(new_price), 2)
        except ValueError:
            print("  Invalid price — kept original.")

    new_cat = input(f"  Category [{target['category']}]: ").strip()
    if new_cat:
        # Accept either a number or a name
        try:
            idx = int(new_cat)
            if 1 <= idx <= len(CATEGORIES):
                target["category"] = CATEGORIES[idx - 1]
        except ValueError:
            if new_cat in CATEGORIES:
                target["category"] = new_cat
            else:
                print("  Unknown category — kept original.")

    save_expenses(expenses)
    print(f"  Updated: {target['item']} — ${target['price']:.2f} [{target['category']}]")


def search_expenses(expenses):
    """Search expenses by keyword in item name."""
    if not expenses:
        print("\n  No expenses to search.")
        return

    keyword = input("\n  Search keyword: ").strip().lower()
    if not keyword:
        return

    results = [e for e in expenses if keyword in e["item"].lower()]
    if not results:
        print(f"  No expenses matching '{keyword}'.")
    else:
        print(f"\n  Found {len(results)} result(s) for '{keyword}':")
        show_expenses(results)


def filter_by_category(expenses):
    """Show expenses filtered by a chosen category."""
    if not expenses:
        print("\n  No expenses to filter.")
        return

    cat = get_category()
    filtered = [e for e in expenses if e["category"] == cat]
    if not filtered:
        print(f"\n  No expenses in '{cat}'.")
    else:
        print(f"\n  Expenses in '{cat}':")
        show_expenses(filtered)


# ============================================================
# SUMMARIES
# ============================================================

def weekly_summary(expenses):
    """Show spending summary for the current week (Mon–Sun)."""
    if not expenses:
        print("\n  No expenses to summarize.")
        return

    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    start_str = start_of_week.strftime("%Y-%m-%d")

    week_expenses = [
        e for e in expenses if e["date"] >= start_str
    ]

    if not week_expenses:
        print(f"\n  No expenses this week (since {start_str}).")
        return

    print(f"\n  === Weekly Summary (since {start_str}) ===")
    by_cat = {}
    total = 0
    for e in week_expenses:
        by_cat[e["category"]] = by_cat.get(e["category"], 0) + e["price"]
        total += e["price"]

    for cat in sorted(by_cat, key=by_cat.get, reverse=True):
        bar = "#" * int(by_cat[cat] / total * 20)
        print(f"  {cat:<15} ${by_cat[cat]:>8.2f}  {bar}")

    print(f"\n  Total this week: ${total:.2f}  ({len(week_expenses)} purchases)")


def monthly_summary(expenses):
    """Show spending summary for the current month."""
    if not expenses:
        print("\n  No expenses to summarize.")
        return

    current_month = datetime.now().strftime("%Y-%m")
    month_expenses = [
        e for e in expenses if e["date"].startswith(current_month)
    ]

    if not month_expenses:
        print(f"\n  No expenses this month ({current_month}).")
        return

    print(f"\n  === Monthly Summary ({current_month}) ===")
    by_cat = {}
    total = 0
    for e in month_expenses:
        by_cat[e["category"]] = by_cat.get(e["category"], 0) + e["price"]
        total += e["price"]

    for cat in sorted(by_cat, key=by_cat.get, reverse=True):
        pct = by_cat[cat] / total * 100
        bar = "#" * int(pct / 5)
        print(f"  {cat:<15} ${by_cat[cat]:>8.2f}  ({pct:>5.1f}%)  {bar}")

    print(f"\n  Total this month: ${total:.2f}  ({len(month_expenses)} purchases)")

    # Daily average
    days_passed = datetime.now().day
    print(f"  Daily average:   ${total / days_passed:.2f}")


# ============================================================
# MAIN MENU
# ============================================================

def print_menu():
    print("\n========= LEDGER =========")
    print("  1. Add expense")
    print("  2. View all expenses")
    print("  3. Delete expense")
    print("  4. Edit expense")
    print("  5. Search expenses")
    print("  6. Filter by category")
    print("  7. Weekly summary")
    print("  8. Monthly summary")
    print("  9. Quit")
    print("==========================")


def main():
    print("\nWelcome to Ledger!")
    expenses = load_expenses()

    if expenses:
        print(f"  Loaded {len(expenses)} saved expense(s).")
    else:
        print("  No saved data found — starting fresh.")

    while True:
        print_menu()
        choice = input("  Choose an option: ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            show_expenses(expenses)
        elif choice == "3":
            delete_expense(expenses)
        elif choice == "4":
            edit_expense(expenses)
        elif choice == "5":
            search_expenses(expenses)
        elif choice == "6":
            filter_by_category(expenses)
        elif choice == "7":
            weekly_summary(expenses)
        elif choice == "8":
            monthly_summary(expenses)
        elif choice == "9":
            save_expenses(expenses)
            print("\n  Goodbye! Your expenses are saved.\n")
            break
        else:
            print("  Invalid option. Pick 1–9.")


if __name__ == "__main__":
    main()
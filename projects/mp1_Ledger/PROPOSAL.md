## My Project Proposal

**Project name:** Ledger (CLI Expense Tracker)

### What I built
A command-line program where I can record what I buy and how much I spend. I can see a list of my purchases, search and filter them, and get summaries of my spending by week or month. All data saves to a file so nothing is lost between sessions.

### Why I chose this
I want to understand where my money goes after shopping, so I can look back and see my spending habits. A simple command-line tool fits my workflow — I can quickly log a purchase right after I get home.

### Main features
- Add an expense: enter item name, price, and category (date is automatically set to today)
- View all expenses in a formatted table with ID, date, item, category, and price
- Delete an expense by its ID
- Edit an existing expense (change name, price, or category)
- Search expenses by keyword
- Filter expenses by category (Food, Transport, Entertainment, Shopping, Bills, Health, Education, Other)
- See a weekly spending summary with category breakdown
- See a monthly spending summary with percentages and daily average
- Data saves to a CSV file automatically — expenses persist across sessions
- Quit the program cleanly

### How it works
- The program starts by loading any previously saved expenses from `ledger_data.csv`
- A numbered menu lets me pick an action (1–9)
- When I add an expense, I type the item name, price, and pick a category from a numbered list
- The program validates all input — empty names are rejected, non-numeric prices are caught, and invalid menu choices are handled
- Every change (add, edit, delete) saves to the CSV file immediately
- Weekly and monthly summaries use real-time dates from the computer to calculate the current week and month

### What I learned
- How to work with dates using Python's `datetime` module
- How to read and write CSV files with the `csv` module for data persistence
- How to group and filter data using list comprehensions
- How to validate user input with while loops and try/except
- How to organize a program into small, focused functions
- How to use a dictionary to store structured data (each expense is a dict with id, date, item, price, category)

### How the program is organized
- **File persistence functions:** `load_expenses()`, `save_expenses()` — handle reading/writing the CSV
- **Input helpers:** `get_price()`, `get_category()` — validate user input with error handling
- **Core actions:** `add_expense()`, `delete_expense()`, `edit_expense()`, `search_expenses()`, `filter_by_category()` — the main features
- **Summaries:** `weekly_summary()`, `monthly_summary()` — calculate and display spending patterns with category breakdowns
- **Main loop:** `main()` — the menu-driven loop that ties everything together
## My Project Proposal

**Project name:** Simple Account Book (CLI)

### What I'm building
A command-line program where I can record what I buy and how much I spend. I want to see a list of my purchases and get a simple summary of my spending by week or month.

### Why I chose this
I want to understand where my money goes after shopping, so I can look back and see my spending habits.

### Main features
- Add an expense: enter item name, price, and date (date is optional, defaults to today)
- View all expenses in a list
- See a weekly spending summary (total spent each week)
- See a monthly spending summary (total spent each month)
- Quit the program cleanly

### How it works
- The program starts with a menu: Add expense, View expenses, Weekly summary, Monthly summary, Quit
- When I add an expense, I type the name, price, and date (or just press enter for today)
- When I view expenses, I see a list with name, price, and date
- Weekly/monthly summary shows how much I spent in each period

### What I don't know yet
- How to work with dates in Python
- How to group expenses by week or month
- How to save expenses so they don't disappear when I close the program
- How to handle bad input (like wrong price or date)

### Next steps
- Build a basic version that lets me add and list expenses
- Learn how to save data to a file
- Add simple weekly/monthly summaries
- Improve input checking
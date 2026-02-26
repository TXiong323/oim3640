# Account Book - Milestone 1 Prototype
# Goal: log expenses and show a summary


def show_expenses(expenses):
    """Print all logged expenses and the total."""
    print("\n--- Your Expenses ---")
    for item in expenses:
        print(f"  {item['name']}: ${item['price']:.2f}")
    
    total = sum(item['price'] for item in expenses)
    print(f"---------------------")
    print(f"  Total: ${total:.2f}")
    print()


def main():
    expenses = []  # This list stores all your expenses

    print("=== Account Book ===")
    print("Log your expenses below.")
    print("Type 'done' when you're finished.\n")

    while True:
        # Ask for item name
        name = input("What did you buy? (or type 'done' to finish): ").strip()
        
        if name.lower() == 'done':
            break
        
        if name == "":
            print("Item name can't be empty. Try again.\n")
            continue

        # Ask for price
        price_input = input(f"How much did '{name}' cost? $").strip()
        
        try:
            price = float(price_input)
            if price < 0:
                print("Price can't be negative. Try again.\n")
                continue
        except ValueError:
            print("That doesn't look like a number. Try again.\n")
            continue

        # Save the expense
        expenses.append({'name': name, 'price': price})
        print(f"✓ Added '{name}' for ${price:.2f}\n")

    # Show the results
    if expenses:
        show_expenses(expenses)
    else:
        print("\nNo expenses logged. Goodbye!")


main()
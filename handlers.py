from datetime import datetime

from storage import load_expenses, save_expenses


def add_expense(args):
    """Handle the 'add' command."""
    expenses = load_expenses()

    new_id = max([e["id"] for e in expenses], default=0) + 1

    expense = {
        "id": new_id,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "description": args.description,
        "amount": args.amount,
    }

    expenses.append(expense)
    save_expenses(expenses)
    print(f"Expense added successfully (ID: {new_id})")


def list_expenses(args):
    """Handle the 'list' command."""
    expenses = load_expenses()

    if not expenses:
        print("No expenses found.")
        return

    print(f"{'ID':<4} {'Date':<12} {'Description':<20} {'Amount':>9}")
    print("-" * 48)

    for e in expenses:
        print(
            f"{e['id']:<4} "
            f"{e['date']:<12} "
            f"{e['description']:<20} "
            f"${e['amount']:>8.2f}"
        )


def update_expense(args):
    """Handle the 'update' command."""
    expenses = load_expenses()

    if args.description is None and args.amount is None:
        print("Error: provide --description and/or --amount to update.")
        return

    for e in expenses:
        if e["id"] == args.id:
            if args.description is not None:
                e["description"] = args.description
            if args.amount is not None:
                e["amount"] = args.amount
            save_expenses(expenses)
            print("Expense updated successfully")
            return

    print(f"Error: No expense found with ID {args.id}")


def delete_expense(args):
    """Handle the 'delete' command."""
    expenses = load_expenses()

    for i, e in enumerate(expenses):
        if e["id"] == args.id:
            del expenses[i]
            save_expenses(expenses)
            print("Expense deleted successfully")
            return

    print(f"Error: No expense found with ID {args.id}")


def summary(args):
    """Handle the 'summary' command, with optional --month filter."""
    expenses = load_expenses()

    if args.month is None:
        total = sum(e["amount"] for e in expenses)
        print(f"Total expenses: ${total:.2f}")
        return

    now = datetime.now()
    total = 0.0

    for e in expenses:
        d = datetime.strptime(e["date"], "%Y-%m-%d")
        if d.month == args.month and d.year == now.year:
            total += e["amount"]

    month_name = datetime(now.year, args.month, 1).strftime("%B")
    print(f"Total expenses for {month_name}: ${total:.2f}")
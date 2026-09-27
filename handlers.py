from datetime import datetime

from storage import load_expenses, save_expenses, load_budgets, save_budgets


def _month_total(expenses, month, year):
    """Sum amounts for a given month/year. Internal helper."""
    total = 0.0
    for e in expenses:
        d = datetime.strptime(e["date"], "%Y-%m-%d")
        if d.month == month and d.year == year:
            total += e["amount"]
    return total

def _check_budget_warning(expenses):
    """Print a warning if the current month's total exceeds its budget"""
    now = datetime.now()
    budgets = load_budgets()
    budget = budgets.get(str(now.month))

    if budget is None:
        return # no budget configured for this month - nothing to check

    total = _month_total(expenses, now.month, now.year)
    if total > budget:
        month_name = now.strftime("%B")
        over = total - budget
        print(
            f"Warning: You've exceeded your {month_name} budget "
            f"of ${budget:.2f}"
            f"(spent ${total:.2f}, over by ${over:.2f})"
        )



def add_expense(args):
    """Handle the 'add' command."""
    expenses = load_expenses()

    new_id = max([e["id"] for e in expenses], default=0) + 1

    expense = {
        "id": new_id,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "description": args.description,
        "amount": args.amount,
        "category": args.category
    }

    expenses.append(expense)
    save_expenses(expenses)
    print(f"Expense added successfully (ID: {new_id})")

    _check_budget_warning(expenses)


def list_expenses(args):
    """Handle the 'list' command, with optional
    --category filter"""
    expenses = load_expenses()

    if args.category is not None:
        expenses = [
            e for e in expenses
            if e.get("category", "Uncategorized").lower() == args.category.lower()
        ]

    if not expenses:
        print("No expenses found.")
        return

    print(f"{'ID':<4} {'Date':<12} {'Description':<20} {'Category':<15} {'Amount':>9}")
    print("-" * 64)

    for e in expenses:
        category = e.get("category", "Uncategorized")
        print(
            f"{e['id']:<4} "
            f"{e['date']:<12} "
            f"{e['description']:<20} "
            f"{category:<15} "
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
    total = _month_total(expenses, args.month, now.year)

    month_name = datetime(now.year, args.month, 1).strftime("%B")
    print(f"Total expenses for {month_name}: ${total:.2f}")

    budgets = load_budgets()
    budget = budgets.get(str(args.month))
    if budget is None:
        return

    print(f"Budget for {month_name}: ${budget:.2f}")
    if total > budget:
        over = total - budget
        print(f"Warning: You are ${over:.2f} over budget")
    else:
        remaining = budget - total
        print(f"Remaining: ${remaining:.2f}")


def set_budget(args):
    """Handle the 'set-budget' command"""
    budgets = load_budgets()
    budgets[str(args.month)] = args.amount
    save_budgets(budgets)

    month_name = datetime(datetime.now().year, args.month, 1).strftime("%B")
    print(f"Budget for {month_name} set to ${args.amount:.2f}")
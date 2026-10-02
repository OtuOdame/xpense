import json
import os
import csv


DATA_FILE = "expenses.json"

BUDGET_FILE = "budgets.json"


def load_expenses():
    """Return the list of expense dicts, or [] if the file is missing/empty."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        if not isinstance(data, list):
            return []
        return data
    except (json.JSONDecodeError, OSError):
        print("Warning: data file is corrupt or unreadable. Starting fresh.")
        return []


def save_expenses(expenses):
    """Write the expense list back to disk as JSON."""
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=2)


def load_budgets():
    """Return a dict mapping month number (as string) to budget amount."""
    if not os.path.exists(BUDGET_FILE):
        return {}
    try:
        with open(BUDGET_FILE, "r") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return {}
        return data
    except (json.JSONDecodeError, OSError):
        print("Warning: budget file is corrupt or unreadable. Starting fresh.")
        return {}


def save_budgets(budgets):
    """Write the budget dict back to disk as JSON."""
    with open(BUDGET_FILE, "w") as f:
        json.dump(budgets, f, indent=2)


def export_to_csv(expenses, filepath):
    """Write expenses to a CSV file. Returns the number of rows written."""
    fieldnames = ["id", "date", "description", "category", "amount"]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        count = 0
        for e in expenses:
            writer.writerow({
                "id": e["id"],
                "date": e["date"],
                "description": e["description"],
                "category": e.get("category", "Uncategorized"),
                "amount": e["amount"],
            })
            count += 1
            
    return count
import json
import os


DATA_FILE = "expenses.json"


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
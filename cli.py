import argparse

from handlers import (
    add_expense,
    list_expenses,
    update_expense,
    delete_expense,
    summary,
    set_budget,
    export_expenses,
)
from validators import positive_float


def main():
    parser = argparse.ArgumentParser(description="Expense Tracker")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # ---- add ----
    add_parser = subparsers.add_parser("add", help="Add a new expense")
    add_parser.add_argument(
        "--description", required=True, help="What the expense was for"
    )
    add_parser.add_argument(
        "--amount",
        type=positive_float,
        required=True,
        help="Amount (positive number)",
    )
    add_parser.add_argument(
        "--category",
        default="Uncategorized",
        help="Category (default: Uncategorized)",
    )
    add_parser.set_defaults(func=add_expense)

    # ---- list ----
    list_parser = subparsers.add_parser("list", help="List all expenses")
    list_parser.add_argument(
        "--category",
        help="Filter to a single category (case-insensitive)"
    )
    list_parser.set_defaults(func=list_expenses)

    # ---- update ----
    update_parser = subparsers.add_parser("update", help="Update an expense")
    update_parser.add_argument("--id", type=int, required=True, help="Expense ID")
    update_parser.add_argument("--description", help="New description")
    update_parser.add_argument("--amount", type=positive_float, help="New amount")
    update_parser.set_defaults(func=update_expense)

    # ---- delete ----
    delete_parser = subparsers.add_parser("delete", help="Delete an expense")
    delete_parser.add_argument("--id", type=int, required=True, help="Expense ID")
    delete_parser.set_defaults(func=delete_expense)

    # ---- summary ----
    summary_parser = subparsers.add_parser("summary", help="Show expense summary")
    summary_parser.add_argument(
        "--month",
        type=int,
        choices=range(1, 13),
        help="Filter by month (1-12), current year only",
    )
    summary_parser.set_defaults(func=summary)

    # ---- set-budget ----
    set_budget_parser = subparsers.add_parser(
        "set-budget", help="Set a budget for a month"
    )
    set_budget_parser.add_argument(
        "--month",
        type=int,
        choices=range(1, 13),
        required=True,
        help="Month number (1-12)",
    )
    set_budget_parser.add_argument(
        "--amount",
        type=positive_float,
        required=True,
        help="Budget amount (positive number)",
    )
    set_budget_parser.set_defaults(func=set_budget)

    # --- export ---
    export_parser = subparsers.add_parser(
        "export", help="Export expenses to a CSV file"
    )
    export_parser.add_argument(
        "--file",
        default="expenses.csv",
        help="Output path (default: expenses.csv)"
    )
    export_parser.set_defaults(func=export_expenses)

    # ---- run ----
    args = parser.parse_args()
    args.func(args)
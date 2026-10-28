# Expense Tracker

A small command-line expense tracker written in plain Python. Expenses are kept in a
local JSON file, with support for categories, monthly summaries, monthly budgets, and
CSV export.

No third-party runtime dependencies — only the standard library.

## Features

- Add, list, update and delete expenses
- Optional category per expense, with case-insensitive filtering
- Monthly summary, with budget comparison when a budget is set
- Over-budget warning when adding an expense in a month with a budget
- Export all expenses to CSV

## Requirements

- Python 3.8 or newer
- `pytest` (tests only)

## Usage

Run commands through `main.py`:

```bash
python main.py <command> [options]
```

| Command | Description |
| --- | --- |
| `add --description TEXT --amount NUM [--category TEXT]` | Add an expense dated today |
| `list [--category TEXT]` | List expenses, optionally filtered by category |
| `update --id N [--description TEXT] [--amount NUM]` | Update an existing expense |
| `delete --id N` | Delete an expense |
| `summary [--month N]` | Total expenses, optionally for one month |
| `set-budget --month N --amount NUM` | Set a budget for a month |
| `export [--file PATH]` | Export expenses to CSV (default `expenses.csv`) |

Examples:

```bash
python main.py add --description "Lunch" --amount 12.50 --category Food
python main.py list --category food
python main.py summary --month 9
python main.py set-budget --month 10 --amount 500
python main.py update --id 2 --amount 15
python main.py export --file october.csv
```

`--amount` must be greater than zero. `--month` is a number from 1 to 12.

## Data files

Both files live in the directory the command is run from:

- `expenses.json` — the expense list
- `budgets.json` — budgets keyed by month, created on first use

If either file is missing, the tracker starts with an empty list. If a file is
unreadable or corrupt, a warning is printed and it starts fresh.

## Notes

- Expenses are dated automatically when added; there is no option to backdate one.
- `summary --month` always uses the current year.
- Budgets are keyed by month number only, so a budget is not tied to a year.

## Running the tests

From the repository root:

```bash
python -m pytest
```

## Project layout

| File | Purpose |
| --- | --- |
| `main.py` | Entry point |
| `cli.py` | Argument parser and command wiring |
| `handlers.py` | Command implementations |
| `storage.py` | JSON and CSV persistence |
| `validators.py` | Argument validation |
| `tests/` | pytest suite, with storage redirected to a temp directory |

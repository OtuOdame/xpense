import argparse

from handlers import add_expense, delete_expense, update_expense, summary, set_budget


def test_add_expense_creates_new_expense(temp_storage, capsys):
    args = argparse.Namespace(description="Lunch", amount=20.0, category="Food")
    add_expense(args)

    captured = capsys.readouterr()
    assert "Expense added successfully (ID: 1)" in captured.out


    # Verify it was actually written
    from storage import load_expenses
    expenses = load_expenses()
    assert len(expenses) == 1
    assert expenses[0]["description"] == "Lunch"
    assert expenses[0]["amount"] == 20.0
    assert expenses[0]["category"] == "Food"
    assert expenses[0]["id"] == 1


def test_add_expense_increments_id(temp_storage):
    add_expense(argparse.Namespace(description="A", amount=1.0, category="X"))
    add_expense(argparse.Namespace(description="B", amount=2.0, category="X"))

    from storage import load_expenses
    expenses = load_expenses()
    assert [e["id"] for e in expenses] == [1, 2]


def test_add_expense_warns_when_over_budget(temp_storage, capsys):
    from storage import save_budgets
    from datetime import datetime
    current_month = str(datetime.now().month)
    save_budgets({current_month: 50.0})

    args = argparse.Namespace(description="Fancy dinner", amount=75.0, category="Food")
    add_expense(args)

    captured = capsys.readouterr()
    assert "Expense added successfully" in captured.out
    assert "Warning: You've exceeded" in captured.out
    assert "over by" in captured.out


def test_add_expense_no_warning_without_budget(temp_storage, capsys):
    args = argparse.Namespace(description="Lunch", amount=20.0, category="Food")
    add_expense(args)

    captured = capsys.readouterr()
    assert "Warning" not in captured.out


def test_delete_expense_not_found(temp_storage, capsys):
    args = argparse.Namespace(id=999)
    delete_expense(args)

    captured = capsys.readouterr()
    assert "No expense found with ID 999" in captured.out


def test_delete_expense_removes_it(temp_storage):
    from storage import save_expenses, load_expenses
    save_expenses([
        {"id": 1, "date": "2026-09-26", "description": "A", "amount": 10.0},
        {"id": 2, "date": "2026-09-26", "description": "B", "amount": 20.0},
    ])

    delete_expense(argparse.Namespace(id=1))

    remaining = load_expenses()
    assert len(remaining) == 1
    assert remaining[0]["id"] == 2


def test_summary_shows_budget_when_set(temp_storage, capsys):
    from storage import save_expenses, save_budgets
    from datetime import datetime
    year = datetime.now().year
    month = datetime.now().month

    save_expenses([
        {"id": 1, "date": f"{year}-{month:02d}-15", "description": "A", "amount": 30.0},
    ])
    save_budgets({str(month): 100.0})

    summary(argparse.Namespace(month=month))

    captured = capsys.readouterr()
    assert "Total expenses for" in captured.out
    assert "Budget for" in captured.out
    assert "Remaining: $" in captured.out
    assert "Warning" not in captured.out

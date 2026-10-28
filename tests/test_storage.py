from storage import load_expenses, save_expenses, load_budgets, save_budgets


def test_load_expenses_returns_empty_list_when_file_missing(tmp_path, monkeypatch):
    monkeypatch.setattr("storage.DATA_FILE", str(tmp_path / "expenses.json"))
    assert load_expenses() == []

def test_save_then_load_expenses_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setattr("storage.DATA_FILE", str(tmp_path / "expenses.json"))

    data = [
        {"id": 1, "date": "2026-09-26", "description": "Lunch", "amount": 20.0},
        {"id": 2, "date": "2026-09-26", "description": "Bus", "amount": 2.5},
    ]
    save_expenses(data)
    assert load_expenses() == data

def test_load_budgets_returns_empty_dict_when_file_missing(tmp_path, monkeypatch):
    monkeypatch.setattr("storage.BUDGET_FILE", str(tmp_path / "budgets.json"))
    assert load_budgets() == {}

def test_save_then_load_budgets_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setattr("storage.BUDGET_FILE", str(tmp_path / "budgets.json"))

    data = {"9": 100.0, "10": 200.0}
    save_budgets(data)
    assert load_budgets() == data
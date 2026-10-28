import pytest

@pytest.fixture
def temp_storage(tmp_path, monkeypatch):
    """Redirect storage to a temp folder for this test only."""
    monkeypatch.setattr("storage.DATA_FILE", str(tmp_path / "expenses.json"))
    monkeypatch.setattr("storage.BUDGET_FILE", str(tmp_path / "budgets.json"))

@pytest.fixture
def sample_expenses():
    """A couple of expenses for tests that need existing data."""
    return [
        {
            "id": 1,
            "date": "2026-09-15",
            "description": "Lunch",
            "amount": 20.0,
            "category": "Food",
        },
        {
            "id": 2,
            "date": "2026-09-20",
            "description": "Bus",
            "amount": 2.5,
            "category": "Transport",
        },
    ]
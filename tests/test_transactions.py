import pytest
from features.transactions import add_transaction, view_transactions
from database.db_utils import fetch_query, execute_query

@pytest.fixture
def setup_test_transactions():
    execute_query("DELETE FROM transactions")
    execute_query("INSERT INTO transactions (user_id, amount, category, date, type) VALUES (?, ?, ?, ?, ?)", 
                  (1, 500, "Food", "2024-12-19", "expense"))
    yield
    execute_query("DELETE FROM transactions")

def test_add_transaction(monkeypatch):
    def mock_input(prompt):
        inputs = {
            "Enter your user ID: ": "1",
            "Enter amount: ": "1000",
            "Enter category (e.g., Food, Rent): ": "Salary",
            "Enter date (YYYY-MM-DD): ": "2024-12-19",
            "Enter type (income/expense): ": "income"
        }
        return inputs[prompt]

    
    monkeypatch.setattr('builtins.input', mock_input)
    add_transaction()
    
    transactions = fetch_query("SELECT * FROM transactions WHERE category = ?", ("Salary",))
    assert len(transactions) == 1

def test_view_transactions(setup_test_transactions, monkeypatch, capsys):
    monkeypatch.setattr('builtins.input', lambda _: "1")
    view_transactions()
    
    captured = capsys.readouterr()
    assert "Food" in captured.out

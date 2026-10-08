import json

from banking.account import SavingsAccount, CheckingAccount
from banking.ledger import Ledger
from banking.persistence import (
    save_accounts_to_json,
    load_accounts_from_json,
    save_transactions_to_csv,
    load_transactions_from_csv,
)


def test_save_accounts_to_json(tmp_path):
    ledger = Ledger()

    ledger.add_account(
        SavingsAccount("S001", "Alice", 1000)
    )

    ledger.add_account(
        CheckingAccount("C001", "Bob", 500)
    )

    filename = tmp_path / "accounts.json"

    save_accounts_to_json(ledger, filename)

    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    assert len(data) == 2
    assert data[0]["account_id"] == "S001"
    assert data[0]["owner"] == "Alice"
    assert data[0]["balance"] == 1000
    assert data[0]["account_type"] == "SavingsAccount"

    assert data[1]["account_id"] == "C001"
    assert data[1]["owner"] == "Bob"
    assert data[1]["balance"] == 500
    assert data[1]["account_type"] == "CheckingAccount"


def test_load_accounts_from_json(tmp_path):
    filename = tmp_path / "accounts.json"

    data = [
        {
            "account_id": "S001",
            "owner": "Alice",
            "balance": 1500,
            "account_type": "SavingsAccount",
        },
        {
            "account_id": "C001",
            "owner": "Bob",
            "balance": 700,
            "account_type": "CheckingAccount",
        },
    ]

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file)

    ledger = load_accounts_from_json(filename)

    savings = ledger.get_account("S001")
    checking = ledger.get_account("C001")

    assert isinstance(savings, SavingsAccount)
    assert isinstance(checking, CheckingAccount)

    assert savings.owner == "Alice"
    assert savings.balance == 1500

    assert checking.owner == "Bob"
    assert checking.balance == 700


def test_load_accounts_unknown_type(tmp_path):
    filename = tmp_path / "accounts.json"

    data = [
        {
            "account_id": "X001",
            "owner": "Unknown",
            "balance": 100,
            "account_type": "UnknownAccount",
        }
    ]

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file)

    try:
        load_accounts_from_json(filename)
        assert False
    except ValueError as error:
        assert "Unknown account type" in str(error)


def test_save_transactions_to_csv(tmp_path):
    filename = tmp_path / "transactions.csv"

    transactions = [
        {
            "account_id": "S001",
            "transaction_type": "deposit",
            "amount": 500,
        },
        {
            "account_id": "S001",
            "transaction_type": "withdraw",
            "amount": 200,
        },
    ]

    save_transactions_to_csv(transactions, filename)

    assert filename.exists()

    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()

    assert "account_id,transaction_type,amount" in content
    assert "S001,deposit,500" in content
    assert "S001,withdraw,200" in content


def test_load_transactions_from_csv(tmp_path):
    filename = tmp_path / "transactions.csv"

    with open(filename, "w", newline="", encoding="utf-8") as file:
        file.write(
            "account_id,transaction_type,amount\n"
            "S001,deposit,500\n"
            "S001,withdraw,200\n"
        )

    transactions = load_transactions_from_csv(filename)

    assert len(transactions) == 2

    assert transactions[0]["account_id"] == "S001"
    assert transactions[0]["transaction_type"] == "deposit"
    assert transactions[0]["amount"] == 500.0

    assert transactions[1]["account_id"] == "S001"
    assert transactions[1]["transaction_type"] == "withdraw"
    assert transactions[1]["amount"] == 200.0
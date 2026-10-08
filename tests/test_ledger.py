import pytest

from banking.account import SavingsAccount, CheckingAccount
from banking.exceptions import (
    AccountNotFoundError,
    DuplicateAccountError,
    InvalidAmountError,
    InsufficientFundsError,
)
from banking.ledger import Ledger


def test_add_and_get_account():
    ledger = Ledger()
    account = SavingsAccount("S001", "Alice", 1000)

    ledger.add_account(account)

    result = ledger.get_account("S001")

    assert result is account
    assert result.balance == 1000


def test_add_duplicate_account_raises_error():
    ledger = Ledger()

    account1 = SavingsAccount("S001", "Alice", 1000)
    account2 = CheckingAccount("S001", "Bob", 500)

    ledger.add_account(account1)

    with pytest.raises(DuplicateAccountError):
        ledger.add_account(account2)


def test_get_missing_account_raises_error():
    ledger = Ledger()

    with pytest.raises(AccountNotFoundError):
        ledger.get_account("S999")


def test_remove_account():
    ledger = Ledger()
    account = SavingsAccount("S001", "Alice", 1000)

    ledger.add_account(account)
    ledger.remove_account("S001")

    with pytest.raises(AccountNotFoundError):
        ledger.get_account("S001")


def test_remove_missing_account_raises_error():
    ledger = Ledger()

    with pytest.raises(AccountNotFoundError):
        ledger.remove_account("S999")


def test_get_all_accounts():
    ledger = Ledger()

    account1 = SavingsAccount("S001", "Alice", 1000)
    account2 = CheckingAccount("C001", "Bob", 500)

    ledger.add_account(account1)
    ledger.add_account(account2)

    accounts = ledger.get_all_accounts()

    assert len(accounts) == 2
    assert account1 in accounts
    assert account2 in accounts


def test_ledger_deposit():
    ledger = Ledger()
    account = SavingsAccount("S001", "Alice", 1000)

    ledger.add_account(account)
    ledger.deposit("S001", 500)

    assert account.balance == 1500


def test_ledger_deposit_invalid_amount():
    ledger = Ledger()
    account = SavingsAccount("S001", "Alice", 1000)

    ledger.add_account(account)

    with pytest.raises(InvalidAmountError):
        ledger.deposit("S001", -100)


def test_ledger_withdraw():
    ledger = Ledger()
    account = SavingsAccount("S001", "Alice", 1000)

    ledger.add_account(account)
    ledger.withdraw("S001", 400)

    assert account.balance == 600


def test_ledger_withdraw_insufficient_funds():
    ledger = Ledger()
    account = SavingsAccount("S001", "Alice", 100)

    ledger.add_account(account)

    with pytest.raises(InsufficientFundsError):
        ledger.withdraw("S001", 200)


def test_ledger_withdraw_missing_account():
    ledger = Ledger()

    with pytest.raises(AccountNotFoundError):
        ledger.withdraw("S999", 100)
import pytest

from banking.account import SavingsAccount, CheckingAccount
from banking.exceptions import (
    InvalidAmountError,
    InsufficientFundsError,
)


def test_savings_account_creation():
    account = SavingsAccount("S001", "Alice", 1000)

    assert account.account_id == "S001"
    assert account.owner == "Alice"
    assert account.balance == 1000


def test_checking_account_creation():
    account = CheckingAccount("C001", "Bob", 2000)

    assert account.account_id == "C001"
    assert account.owner == "Bob"
    assert account.balance == 2000


def test_deposit_increases_balance():
    account = SavingsAccount("S001", "Alice", 1000)

    account.deposit(500)

    assert account.balance == 1500


def test_negative_deposit_raises_error():
    account = SavingsAccount("S001", "Alice", 1000)

    with pytest.raises(InvalidAmountError):
        account.deposit(-100)


def test_zero_deposit_raises_error():
    account = SavingsAccount("S001", "Alice", 1000)

    with pytest.raises(InvalidAmountError):
        account.deposit(0)


def test_savings_withdraw():
    account = SavingsAccount("S001", "Alice", 1000)

    account.withdraw(400)

    assert account.balance == 600


def test_savings_insufficient_funds():
    account = SavingsAccount("S001", "Alice", 100)

    with pytest.raises(InsufficientFundsError):
        account.withdraw(200)


def test_savings_invalid_withdrawal():
    account = SavingsAccount("S001", "Alice", 1000)

    with pytest.raises(InvalidAmountError):
        account.withdraw(0)


def test_checking_withdraw():
    account = CheckingAccount("C001", "Bob", 1000)

    account.withdraw(700)

    assert account.balance == 300


def test_checking_allows_overdraft():
    account = CheckingAccount("C001", "Bob", 1000)

    account.withdraw(1200)

    assert account.balance == -200


def test_checking_overdraft_limit():
    account = CheckingAccount("C001", "Bob", 1000)

    with pytest.raises(InsufficientFundsError):
        account.withdraw(1600)


def test_checking_invalid_withdrawal():
    account = CheckingAccount("C001", "Bob", 1000)

    with pytest.raises(InvalidAmountError):
        account.withdraw(-50)
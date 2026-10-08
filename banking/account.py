from abc import ABC, abstractmethod

from banking.exceptions import (
    InvalidAmountError,
    InsufficientFundsError
)


class Account(ABC):

    def __init__(self, account_id: str, owner: str, balance: float = 0):
        self._account_id = account_id
        self._owner = owner
        self._balance = balance

    @property
    def account_id(self):
        return self._account_id

    @property
    def owner(self):
        return self._owner

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount: float):
        if amount <= 0:
            raise InvalidAmountError(
                "Deposit amount must be positive"
            )

        self._balance += amount

    @abstractmethod
    def withdraw(self, amount: float):
        pass


class SavingsAccount(Account):

    def withdraw(self, amount: float):
        if amount <= 0:
            raise InvalidAmountError(
                "Withdrawal amount must be positive"
            )

        if amount > self._balance:
            raise InsufficientFundsError(
                "Insufficient funds in savings account"
            )

        self._balance -= amount


class CheckingAccount(Account):

    def withdraw(self, amount: float):
        if amount <= 0:
            raise InvalidAmountError(
                "Withdrawal amount must be positive"
            )

        overdraft_limit = 500

        if amount > self._balance + overdraft_limit:
            raise InsufficientFundsError(
                "Overdraft limit exceeded"
            )

        self._balance -= amount
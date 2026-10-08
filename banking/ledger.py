from banking.account import Account
from banking.exceptions import (
    AccountNotFoundError,
    DuplicateAccountError
)


class Ledger:

    def __init__(self):
        self._accounts = {}

    def add_account(self, account: Account):
        if account.account_id in self._accounts:
            raise DuplicateAccountError(
                f"Account {account.account_id} already exists"
            )

        self._accounts[account.account_id] = account

    def get_account(self, account_id: str) -> Account:
        if account_id not in self._accounts:
            raise AccountNotFoundError(
                f"Account {account_id} not found"
            )

        return self._accounts[account_id]

    def remove_account(self, account_id: str):
        if account_id not in self._accounts:
            raise AccountNotFoundError(
                f"Account {account_id} not found"
            )

        del self._accounts[account_id]

    def get_all_accounts(self):
        return list(self._accounts.values())

    def deposit(self, account_id: str, amount: float):
        account = self.get_account(account_id)
        account.deposit(amount)

    def withdraw(self, account_id: str, amount: float):
        account = self.get_account(account_id)
        account.withdraw(amount)
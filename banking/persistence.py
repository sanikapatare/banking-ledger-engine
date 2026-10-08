import csv
import json

from banking.account import SavingsAccount, CheckingAccount
from banking.ledger import Ledger


def save_accounts_to_json(ledger: Ledger, filename: str):
    accounts = []

    for account in ledger.get_all_accounts():
        account_type = type(account).__name__

        accounts.append(
            {
                "account_id": account.account_id,
                "owner": account.owner,
                "balance": account.balance,
                "account_type": account_type,
            }
        )

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(accounts, file, indent=4)


def load_accounts_from_json(filename: str) -> Ledger:
    ledger = Ledger()

    with open(filename, "r", encoding="utf-8") as file:
        accounts = json.load(file)

    for data in accounts:
        if data["account_type"] == "SavingsAccount":
            account = SavingsAccount(
                data["account_id"],
                data["owner"],
                data["balance"],
            )

        elif data["account_type"] == "CheckingAccount":
            account = CheckingAccount(
                data["account_id"],
                data["owner"],
                data["balance"],
            )

        else:
            raise ValueError(
                f"Unknown account type: {data['account_type']}"
            )

        ledger.add_account(account)

    return ledger


def save_transactions_to_csv(transactions: list, filename: str):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "account_id",
                "transaction_type",
                "amount",
            ],
        )

        writer.writeheader()
        writer.writerows(transactions)


def load_transactions_from_csv(filename: str) -> list:
    with open(filename, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        transactions = []

        for row in reader:
            transactions.append(
                {
                    "account_id": row["account_id"],
                    "transaction_type": row["transaction_type"],
                    "amount": float(row["amount"]),
                }
            )

        return transactions
# Banking Ledger Engine

A Python-based banking ledger system demonstrating object-oriented programming, custom exception handling, JSON/CSV persistence, and automated testing with pytest.

## Project Overview

The Banking Ledger Engine models a simple banking system using an object-oriented design.

The system supports:

- Savings accounts
- Checking accounts
- Deposits
- Withdrawals
- Checking account overdraft
- Account management through a central ledger
- JSON account persistence
- CSV transaction persistence
- Custom exception handling
- Automated unit testing

## OOP Concepts Used

### Abstraction

`Account` is an abstract base class using Python's `ABC` and `abstractmethod`.

```python
class Account(ABC):
    @abstractmethod
    def withdraw(self, amount: float):
        pass
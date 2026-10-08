class BankingError(Exception):
    """Base exception for the banking application."""
    pass


class InvalidAmountError(BankingError):
    """Raised when amount is invalid."""
    pass


class InsufficientFundsError(BankingError):
    """Raised when balance is insufficient."""
    pass


class AccountNotFoundError(BankingError):
    """Raised when account does not exist."""
    pass


class DuplicateAccountError(BankingError):
    """Raised when account already exists."""
    pass
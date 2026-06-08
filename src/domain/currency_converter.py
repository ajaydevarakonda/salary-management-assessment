from decimal import Decimal
from typing import Protocol


class CurrencyConverter(Protocol):
    """Converts monetary amounts from any supported currency to USD."""

    def to_usd(self, amount: Decimal, from_currency: str) -> Decimal:
        """Return the USD equivalent of amount in from_currency."""
        ...

from decimal import Decimal


_RATES_TO_USD: dict[str, Decimal] = {
    "USD": Decimal("1"),
    "INR": Decimal("0.012"),
    "GBP": Decimal("1.27"),
    "EUR": Decimal("1.08"),
    "CAD": Decimal("0.73"),
    "AUD": Decimal("0.65"),
    "SGD": Decimal("0.74"),
    "BRL": Decimal("0.20"),
}


class FixedRateCurrencyConverter:
    """Converts amounts to USD using hardcoded exchange rates."""

    def to_usd(self, amount: Decimal, from_currency: str) -> Decimal:
        """Return the USD equivalent of amount, rounded to 2 decimal places."""
        if from_currency not in _RATES_TO_USD:
            raise ValueError(f"Unsupported currency: {from_currency}")
        return (amount * _RATES_TO_USD[from_currency]).quantize(Decimal("0.01"))

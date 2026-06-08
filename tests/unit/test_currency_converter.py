import pytest
from decimal import Decimal

from src.infrastructure.fixed_rate_currency_converter import FixedRateCurrencyConverter


class TestFixedRateCurrencyConverter:
    def test_usd_to_usd_returns_same_amount(self):
        converter = FixedRateCurrencyConverter()
        assert converter.to_usd(Decimal("1000"), "USD") == Decimal("1000.00")

    def test_inr_to_usd_converts_correctly(self):
        converter = FixedRateCurrencyConverter()
        assert converter.to_usd(Decimal("1000"), "INR") == Decimal("12.00")

    def test_gbp_to_usd_converts_correctly(self):
        converter = FixedRateCurrencyConverter()
        assert converter.to_usd(Decimal("100"), "GBP") == Decimal("127.00")

    def test_eur_to_usd_converts_correctly(self):
        converter = FixedRateCurrencyConverter()
        assert converter.to_usd(Decimal("100"), "EUR") == Decimal("108.00")

    def test_raises_for_unknown_currency(self):
        converter = FixedRateCurrencyConverter()
        with pytest.raises(ValueError, match="Unsupported currency: XYZ"):
            converter.to_usd(Decimal("100"), "XYZ")

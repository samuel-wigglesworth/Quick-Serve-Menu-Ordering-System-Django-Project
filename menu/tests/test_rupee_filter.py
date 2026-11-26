"""Unit tests for the rupee custom template filter."""
from decimal import Decimal

import pytest

from menu.templatetags.rupee_filter import _format_indian, rupee


# ---------------------------------------------------------------------------
# _format_indian helper
# ---------------------------------------------------------------------------

class TestFormatIndian:
    def test_three_digits_no_comma(self):
        assert _format_indian("999") == "999"

    def test_four_digits(self):
        assert _format_indian("1000") == "1,000"

    def test_five_digits(self):
        assert _format_indian("12345") == "12,345"

    def test_six_digits(self):
        assert _format_indian("123456") == "1,23,456"

    def test_seven_digits(self):
        assert _format_indian("1234567") == "12,34,567"

    def test_eight_digits(self):
        assert _format_indian("12345678") == "1,23,45,678"

    def test_one_digit(self):
        assert _format_indian("5") == "5"

    def test_two_digits(self):
        assert _format_indian("50") == "50"


# ---------------------------------------------------------------------------
# rupee filter
# ---------------------------------------------------------------------------

class TestRupeeFilter:
    # --- None / falsy inputs ---

    def test_none_returns_zero(self):
        assert rupee(None) == "₹0.00"

    def test_empty_string_returns_zero(self):
        assert rupee("") == "₹0.00"

    def test_invalid_string_returns_zero(self):
        assert rupee("abc") == "₹0.00"

    # --- Integer inputs ---

    def test_zero_int(self):
        assert rupee(0) == "₹0.00"

    def test_one_thousand(self):
        assert rupee(1000) == "₹1,000.00"

    def test_one_lakh(self):
        assert rupee(100000) == "₹1,00,000.00"

    def test_ten_lakh(self):
        assert rupee(1000000) == "₹10,00,000.00"

    # --- Float inputs ---

    def test_float_with_decimals(self):
        assert rupee(123456.78) == "₹1,23,456.78"

    def test_float_rounds_to_two_places(self):
        # 1.005 as float may be imprecise; use Decimal for precision test below
        result = rupee(1.5)
        assert result == "₹1.50"

    # --- Decimal inputs ---

    def test_decimal_zero(self):
        assert rupee(Decimal("0")) == "₹0.00"

    def test_decimal_simple(self):
        assert rupee(Decimal("500.00")) == "₹500.00"

    def test_decimal_thousands(self):
        assert rupee(Decimal("1234.56")) == "₹1,234.56"

    def test_decimal_lakh(self):
        assert rupee(Decimal("123456.78")) == "₹1,23,456.78"

    def test_decimal_crore(self):
        assert rupee(Decimal("12345678.00")) == "₹1,23,45,678.00"

    # --- String inputs ---

    def test_string_integer(self):
        assert rupee("5000") == "₹5,000.00"

    def test_string_decimal(self):
        assert rupee("99999.99") == "₹99,999.99"

    # --- Rupee symbol and format guarantees ---

    def test_result_starts_with_rupee_symbol(self):
        assert rupee(Decimal("42")).startswith("₹")

    def test_result_has_two_decimal_places(self):
        result = rupee(Decimal("1234"))
        assert result.endswith(".00")

    def test_no_dollar_sign(self):
        assert "$" not in rupee(Decimal("9999999"))

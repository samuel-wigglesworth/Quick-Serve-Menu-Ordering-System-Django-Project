from decimal import Decimal, InvalidOperation

from django import template

register = template.Library()


def _format_indian(integer_str: str) -> str:
    """Format an integer string using Indian number grouping.

    Indian grouping: rightmost 3 digits form the first group, then every
    2 digits to the left.

    Examples:
        "123456"   -> "1,23,456"
        "1234567"  -> "12,34,567"
        "12345"    -> "12,345"
        "1000"     -> "1,000"
        "999"      -> "999"
    """
    if len(integer_str) <= 3:
        return integer_str

    # Split off the rightmost 3 digits.
    right = integer_str[-3:]
    left = integer_str[:-3]

    # Group the remaining digits in pairs from the right.
    groups = []
    while len(left) > 2:
        groups.append(left[-2:])
        left = left[:-2]
    if left:
        groups.append(left)

    groups.reverse()
    return ",".join(groups) + "," + right


@register.filter(name="rupee")
def rupee(value):
    """Format *value* as an Indian-Rupee string (e.g. ₹1,23,456.78).

    Accepts int, float, Decimal, or a string representation of a number.
    Returns "₹0.00" for None, empty string, or any value that cannot be
    converted to a Decimal.
    """
    if value is None or value == "":
        return "₹0.00"

    try:
        amount = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        return "₹0.00"

    # Format with exactly 2 decimal places.
    formatted = f"{amount:.2f}"

    # Split into integer and decimal parts.
    integer_part, decimal_part = formatted.split(".")

    # Handle negative values: preserve sign, format absolute value.
    negative = integer_part.startswith("-")
    if negative:
        integer_part = integer_part[1:]

    grouped = _format_indian(integer_part)

    sign = "-" if negative else ""
    return f"₹{sign}{grouped}.{decimal_part}"

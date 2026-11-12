"""
Tests for payment processing.
"""

import pytest
from shopflow.payments import validate_card_checksum, process_payment


def test_card_validation():
    assert validate_card_checksum("4111111111111111") is True
    assert validate_card_checksum("123") is False


def test_guest_payment_tax_planted_bug():
    """
    PLANTED BUG 2 REPRODUCTION:
    A guest customer checkout has tax_rate=None.
    Multiplying amount * None crashes with:
    TypeError: unsupported operand type(s) for *: 'float' and 'NoneType'
    """
    guest_profile = {
        "customer_id": "guest_892",
        "tax_rate": None,
    }
    result = process_payment(50.0, "USD", guest_profile)
    assert result["status"] == "success"
    assert result["charged_amount"] == 50.0


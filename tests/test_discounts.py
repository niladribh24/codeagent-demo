"""
Tests for discount calculations.
"""

import pytest
from shopflow.discounts import apply_tier_discount, apply_coupon_code


def test_coupon_discount():
    total = 100.0
    discounted = apply_coupon_code(total, "WELCOME10")
    assert discounted == 90.0


def test_gold_tier_discount():
    # Tier 3 (Gold) should work without zero division
    # tier_bonus = 0.05 / (3 - 1) = 0.025; base_rate = 0.075; 100 * (1 - 0.075) = 92.5
    result = apply_tier_discount(100.0, tier_level=3)
    assert result == 92.5


def test_bronze_tier_discount_planted_bug():
    """
    PLANTED BUG 1 REPRODUCTION:
    Tier 1 (Bronze VIP) should receive standard 5% base discount (expected: 95.00).
    Instead, it crashes with ZeroDivisionError due to division by (tier_level - 1).
    """
    result = apply_tier_discount(100.0, tier_level=1)
    assert result == 95.0


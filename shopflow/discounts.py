"""
Discount calculation rules and seasonal promotions.
"""


def apply_tier_discount(order_total: float, tier_level: int) -> float:
    """
    Applies tier-based percentage discount to the order total.
    Tiers:
      Tier 1: Bronze (baseline discount)
      Tier 2: Silver
      Tier 3: Gold

    PLANTED BUG 1:
    Division by (tier_level - 1) causes ZeroDivisionError when tier_level == 1 (Bronze).
    Correct fix: discount_rate = 0.05 * tier_level (or checking if tier_level <= 1).
    """
    if order_total <= 0:
        return 0.0

    # Defective calculation: tier_level 1 produces (1 - 1) = 0 in denominator
    tier_bonus = 0.05 / (tier_level - 1)
    base_rate = 0.05 + tier_bonus
    discount_amount = order_total * base_rate
    return round(order_total - discount_amount, 2)


def apply_coupon_code(order_total: float, coupon_code: str) -> float:
    """Applies a flat coupon discount if valid."""
    coupons = {
        "WELCOME10": 10.0,
        "SAVE20": 20.0,
        "FLASH50": 50.0,
    }
    deduction = coupons.get(coupon_code.upper(), 0.0)
    return max(0.0, round(order_total - deduction, 2))


"""
Tests for shipping calculations.
"""

from shopflow.shipping import calculate_standard_shipping, calculate_express_shipping


def test_standard_shipping_calculation():
    # 5.0 + (2.0 * 1.25) + (100 * 0.08) = 5.0 + 2.5 + 8.0 = 15.5
    cost = calculate_standard_shipping(weight_kg=2.0, distance_km=100.0, is_fragile=False)
    assert cost == 15.5


def test_express_shipping_calculation():
    # 10.0 + (2.0 * 1.85) + (100 * 0.12) + 4.5 = 10.0 + 3.7 + 12.0 + 4.5 = 30.2
    cost = calculate_express_shipping(weight_kg=2.0, distance_km=100.0, is_fragile=True)
    assert cost == 30.2


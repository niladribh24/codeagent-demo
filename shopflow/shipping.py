"""
Shipping rate calculation based on weight, distance, and fragility.
"""


def calculate_standard_shipping(weight_kg: float, distance_km: float, is_fragile: bool = False) -> float:
    """
    Computes standard ground shipping costs.
    Duplicate candidate paired with calculate_express_shipping.
    """
    base_fee = 5.0
    weight_cost = weight_kg * 1.25
    distance_cost = distance_km * 0.08
    subtotal = base_fee + weight_cost + distance_cost
    if is_fragile:
        subtotal += 4.50
    return round(subtotal, 2)


def calculate_express_shipping(weight_kg: float, distance_km: float, is_fragile: bool = False) -> float:
    """
    Computes express priority shipping costs.
    Duplicate candidate paired with calculate_standard_shipping.
    """
    base_fee = 10.0
    weight_cost = weight_kg * 1.85
    distance_cost = distance_km * 0.12
    subtotal = base_fee + weight_cost + distance_cost
    if is_fragile:
        subtotal += 4.50
    return round(subtotal, 2)


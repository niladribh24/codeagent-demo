"""
Inventory management, stock checks, and warehouse reservations.
"""

from typing import List, Tuple

# Mock warehouse inventory balance
INVENTORY_STOCK = {
    "item_101": 50,
    "item_102": 15,
    "item_103": 0,
}


def check_availability(item_id: str, required_qty: int) -> bool:
    """Verifies whether warehouse stock satisfies the required quantity."""
    available = INVENTORY_STOCK.get(item_id, 0)
    return available >= required_qty


def reserve_stock(item_id: str, quantity: int, reserved_list: list = []) -> list:
    """
    Appends an item reservation to the reservation batch.

    PLANTED BUG 3:
    Python default argument trap: 'reserved_list: list = []' is evaluated once at
    function definition time. Subsequent calls reusing the default argument mutate
    the same list, leaking items across distinct customer orders.
    Correct fix: if reserved_list is None: reserved_list = []
    """
    if quantity <= 0:
        return reserved_list

    reserved_list.append((item_id, quantity))
    return reserved_list


def release_stock(item_id: str, quantity: int) -> bool:
    """Restores stock back into the warehouse upon cancellation."""
    if item_id in INVENTORY_STOCK:
        INVENTORY_STOCK[item_id] += quantity
        return True
    return False


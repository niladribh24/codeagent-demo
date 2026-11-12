"""
Tests for warehouse stock reservations.
"""

import pytest
from shopflow.inventory import check_availability, reserve_stock


def test_availability_check():
    assert check_availability("item_101", 10) is True
    assert check_availability("item_103", 1) is False


def test_stock_reservation_isolation_planted_bug():
    """
    PLANTED BUG 3 REPRODUCTION:
    Demonstrates state leakage across distinct calls due to mutable default list argument.
    The first call uses the default list.
    The second call explicitly passes a fresh list.
    The third call reuses the default argument and unexpectedly retains the first call's data!
    """
    # Call 1: Uses default list
    first_order_reservations = reserve_stock("item_101", 2)
    assert len(first_order_reservations) == 1

    # Call 2: Uses independent explicit list
    second_order_reservations = reserve_stock("item_102", 1, [])
    assert len(second_order_reservations) == 1

    # Call 3: Uses default list again (leaks item_101 from Call 1!)
    third_order_reservations = reserve_stock("item_101", 3)
    # Expected for an isolated call: 1 reservation
    # Actual failure: length is 2 because default list was mutated!
    assert len(third_order_reservations) == 1


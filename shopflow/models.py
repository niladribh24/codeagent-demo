"""
Data models representing items, customers, and customer orders.
"""

from typing import List, Optional
from dataclasses import dataclass, field


@dataclass
class Item:
    item_id: str
    name: str
    unit_price: float
    weight_kg: float = 0.5


@dataclass
class Customer:
    customer_id: str
    name: str
    tier_level: int = 1  # 1 = Bronze, 2 = Silver, 3 = Gold
    tax_rate: Optional[float] = None
    email: str = ""


@dataclass
class Order:
    order_id: str
    customer: Customer
    items: List[Item] = field(default_factory=list)
    shipping_distance_km: float = 10.0
    status: str = "pending"

    def calculate_subtotal(self) -> float:
        """Calculate the sum of all item prices in this order."""
        total = 0.0
        for item in self.items:
            total += item.unit_price
        return round(total, 2)

    def total_weight(self) -> float:
        """Calculate total weight of items in kg."""
        return sum(item.weight_kg for item in self.items)


"""
Order processing orchestrator connecting models, discounts, inventory, shipping, and payments.
"""

from typing import Dict, Any
from shopflow.models import Order
from shopflow.discounts import apply_tier_discount, apply_coupon_code
from shopflow.inventory import check_availability, reserve_stock
from shopflow.shipping import calculate_standard_shipping
from shopflow.payments import process_payment


def checkout_order(order: Order, coupon_code: str = "") -> Dict[str, Any]:
    """
    Executes the full checkout pipeline for a customer order.
    Demonstrates inter-module dependencies and function call trees.
    """
    # 1. Calculate items subtotal
    subtotal = order.calculate_subtotal()
    if subtotal <= 0:
        return {"status": "error", "message": "Order is empty"}

    # 2. Check stock and reserve inventory
    for item in order.items:
        if not check_availability(item.item_id, 1):
            return {"status": "error", "message": f"Item {item.item_id} out of stock"}
        reserve_stock(item.item_id, 1)

    # 3. Apply customer tier discount
    discounted = apply_tier_discount(subtotal, order.customer.tier_level)

    # 4. Optional coupon discount
    if coupon_code:
        discounted = apply_coupon_code(discounted, coupon_code)

    # 5. Calculate shipping costs
    shipping = calculate_standard_shipping(
        weight_kg=order.total_weight(),
        distance_km=order.shipping_distance_km
    )

    final_total = round(discounted + shipping, 2)

    # 6. Process payment
    user_profile = {
        "customer_id": order.customer.customer_id,
        "tax_rate": order.customer.tax_rate,
    }
    payment_result = process_payment(final_total, "USD", user_profile)

    order.status = "confirmed" if payment_result.get("status") == "success" else "failed"

    return {
        "order_id": order.order_id,
        "status": order.status,
        "subtotal": subtotal,
        "final_total": final_total,
        "payment": payment_result,
    }


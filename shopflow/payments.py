"""
Payment gateway abstraction and transaction validation.
"""


def validate_card_checksum(card_number: str) -> bool:
    """Performs basic Luhn-like length and character check."""
    digits = [c for c in card_number if c.isdigit()]
    return len(digits) in (15, 16)


def process_payment(amount: float, currency: str, user_profile: dict) -> dict:
    """
    Submits a charge to the payment processor.

    PLANTED BUG 2:
    Does not provide a fallback default for 'tax_rate'. If user_profile['tax_rate']
    is None or omitted, multiplying amount * None raises TypeError.
    Correct fix: tax_rate = user_profile.get("tax_rate") or 0.0
    """
    if amount <= 0:
        return {"status": "rejected", "reason": "Invalid amount"}

    tax_rate = user_profile.get("tax_rate")
    # Defective line: tax_rate can be None
    tax_amount = amount * tax_rate
    final_charge = round(amount + tax_amount, 2)

    return {
        "status": "success",
        "charged_amount": final_charge,
        "currency": currency,
        "transaction_id": f"txn_{int(amount * 100)}",
    }


def refund_payment(transaction_id: str, reason: str = "customer_request") -> dict:
    """Issues a full refund for a settled transaction."""
    return {
        "status": "refunded",
        "transaction_id": transaction_id,
        "reason": reason,
    }


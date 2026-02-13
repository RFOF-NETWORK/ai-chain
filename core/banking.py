# core/banking.py
# de-en: Fiat banking logic (EUR/USD <-> AI/COIN/AIC_LP)

from typing import Dict


def fiat_deposit(username: str, amount: float, currency: str, target_token: str) -> Dict:
    """
    Logical representation of a fiat deposit.
    Real payment processing happens via external providers (PayPal, Stripe, bank_api).
    """
    return {
        "success": True,
        "type": "fiat_deposit",
        "username": username,
        "amount": amount,
        "currency": currency,
        "target_token": target_token
    }


def fiat_withdraw(username: str, amount: float, currency: str, source_token: str) -> Dict:
    """
    Logical representation of a fiat withdrawal.
    """
    return {
        "success": True,
        "type": "fiat_withdraw",
        "username": username,
        "amount": amount,
        "currency": currency,
        "source_token": source_token
    }

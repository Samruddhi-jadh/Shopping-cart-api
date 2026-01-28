# store.py
from typing import Dict
from cart import ShoppingCart  # or import correctly

cart_store: Dict[str, ShoppingCart] = {}
idempotency_store: Dict[str, dict] = {}

def get_cart(cart_id: str) -> ShoppingCart:
    if cart_id not in cart_store:
        cart_store[cart_id] = ShoppingCart()
    return cart_store[cart_id]

def reset_cart(cart_id: str):
    cart_store.pop(cart_id, None)

def reset_all_carts():
    cart_store.clear()
    idempotency_store.clear()

def get_idempotent_response(key: str):
    return idempotency_store.get(key)

def save_idempotent_response(key: str, response: dict):
    idempotency_store[key] = response

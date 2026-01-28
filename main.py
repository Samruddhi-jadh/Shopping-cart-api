from fastapi import FastAPI, HTTPException, Header
from typing import Dict, Optional
from pydantic import BaseModel
from abc import ABC, abstractmethod
# NOTE:
# In production, cart storage and idempotency
# would be moved to store.py or Redis.
# Kept in main.py for simplicity.

# Discount Strategies
# =========================================================



class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float) -> float:
        pass


class NoDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float):
        self.percentage = percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.percentage / 100)


class FlatDiscount(DiscountStrategy):
    def __init__(self, amount: float):
        self.amount = amount

    def apply(self, total: float) -> float:
        return max(0, total - self.amount)


# Shopping Cart
# =========================================================

class ShoppingCart:
    def __init__(self):
        self.items: Dict[str, float] = {}
        self.discount: DiscountStrategy = NoDiscount()

    def add_item(self, name: str, price: float):
        self.items[name] = price

    def set_discount(self, discount: DiscountStrategy):
        self.discount = discount

    def calculate_total(self) -> float:
        total = sum(self.items.values())
        return self.discount.apply(total)


# Request Models
# =========================================================

class ItemRequest(BaseModel):
    name: str
    price: float


class DiscountRequest(BaseModel):
    type: str                 # none | percentage | flat
    value: Optional[float] = None



# App Setup
# =========================================================

app = FastAPI(title="🛒 Shopping Cart API (Multi-User + Idempotency)")

cart_store: Dict[str, ShoppingCart] = {}
idempotency_store: Dict[str, dict] = {}


# Helpers
# =========================================================

def get_cart(cart_id: str) -> ShoppingCart:
    if cart_id not in cart_store:
        cart_store[cart_id] = ShoppingCart()
    return cart_store[cart_id]



# Cart APIs
# =========================================================

@app.post("/cart/{cart_id}/item")
def add_item(
    cart_id: str,
    item: ItemRequest,
    idempotency_key: str = Header(...)
):
    if idempotency_key in idempotency_store:
        return idempotency_store[idempotency_key]

    cart = get_cart(cart_id)
    cart.add_item(item.name, item.price)

    response = {
        "message": "Item added",
        "cart_total": cart.calculate_total()
    }

    idempotency_store[idempotency_key] = response
    return response


@app.get("/cart/{cart_id}/items")
def get_items(cart_id: str):
    cart = get_cart(cart_id)
    return {
        "items": cart.items,
        "total": cart.calculate_total()
    }


@app.post("/cart/{cart_id}/discount")
def apply_discount(cart_id: str, discount: DiscountRequest):
    cart = get_cart(cart_id)

    if discount.type == "none":
        cart.set_discount(NoDiscount())

    elif discount.type == "percentage":
        if discount.value is None:
            raise HTTPException(400, "Percentage value required")
        cart.set_discount(PercentageDiscount(discount.value))

    elif discount.type == "flat":
        if discount.value is None:
            raise HTTPException(400, "Flat value required")
        cart.set_discount(FlatDiscount(discount.value))

    else:
        raise HTTPException(400, "Invalid discount type")

    return {
        "message": "Discount applied",
        "total": cart.calculate_total()
    }


@app.get("/cart/{cart_id}/total")
def get_total(cart_id: str):
    cart = get_cart(cart_id)
    return {"total": cart.calculate_total()}


@app.post("/cart/{cart_id}/reset")
def reset_cart(cart_id: str):
    cart_store.pop(cart_id, None)
    return {"message": "Cart reset"}


# Startup Hook
# =========================================================

@app.on_event("startup")
def reset_all_carts():
    cart_store.clear()
    idempotency_store.clear()
    print("🧹 All carts reset on startup")


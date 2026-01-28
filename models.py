from pydantic import BaseModel

class ItemRequest(BaseModel):
    name: str
    price: float

class DiscountRequest(BaseModel):
    type: str  # "none" | "percentage" | "flat"
    value: float | None = None

from abc import ABC, abstractmethod

class DiscountStrategy(ABC):
    @abstractmethod
    def apply_discount(self, total_price: float) -> float:
        pass


class NoDiscount(DiscountStrategy):
    def apply_discount(self, total_price: float) -> float:
        return total_price


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float):
        self.percentage = percentage

    def apply_discount(self, total_price: float) -> float:
        return total_price * (1 - self.percentage / 100)


class FlatDiscount(DiscountStrategy):
    def __init__(self, amount: float):
        self.amount = amount

    def apply_discount(self, total_price: float) -> float:
        return max(0, total_price - self.amount)


class ShoppingCart:
    def __init__(self):
        self.items = {}
        self.strategy = NoDiscount()

    def add_item(self, name: str, price: float):
        self.items[name] = price

    def set_discount(self, strategy: DiscountStrategy):
        self.strategy = strategy

    def total(self) -> float:
        return self.strategy.apply_discount(sum(self.items.values()))

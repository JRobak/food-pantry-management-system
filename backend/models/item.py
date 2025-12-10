# class Item:
#     def __init__(self, name, category, quantity):
#         self.name = name
#         self.category = category
#         self.quantity = quantity

#     def update_quantity(self, amount):
#         self.quantity += amount
# backend/models/item.py

# backend/models/item.py

from dataclasses import dataclass, asdict


@dataclass
class Item:
    """
    Represents a pantry item in the inventory.
    """

    name: str
    category: str
    quantity: int = 0

    def update_quantity(self, amount: int) -> None:
        """
        Change the quantity by the given amount.
        Positive to add stock, negative to reduce.
        Raises ValueError if result would be negative.
        """
        new_qty = self.quantity + amount
        if new_qty < 0:
            raise ValueError(
                f"Cannot reduce '{self.name}' below zero. "
                f"Current: {self.quantity}, change: {amount}"
            )
        self.quantity = new_qty

    def to_dict(self) -> dict:
        """
        Convert this Item to a plain dict for JSON storage.
        """
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Item":
        """
        Create an Item from a dict (inverse of to_dict).
        """
        return cls(
            name=data["name"],
            category=data["category"],
            quantity=data.get("quantity", 0),
        )

# class Recipient:
#     def __init__(self, name, household_size, notes=""):
#         self.name = name
#         self.household_size = household_size
#         self.notes = notes

# backend/models/recipient.py

# backend/models/recipient.py

from dataclasses import dataclass, field, asdict
from typing import List, Dict


@dataclass
class Recipient:
    """
    Represents a recipient (family/person) who receives food.
    """

    name: str
    household_size: int
    notes: str = ""  # for the GUI "Notes" field
    # Each entry: {"item_name": str, "quantity": int, "timestamp": str}
    received_items: List[Dict] = field(default_factory=list)

    def record_receipt(self, item_name: str, quantity: int, timestamp: str) -> None:
        """
        Record that this recipient received some quantity of an item.
        """
        self.received_items.append(
            {
                "item_name": item_name,
                "quantity": quantity,
                "timestamp": timestamp,
            }
        )

    def to_dict(self) -> dict:
        """
        Convert this Recipient to a plain dict for JSON storage.
        """
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Recipient":
        """
        Create a Recipient from a dict (inverse of to_dict).
        """
        return cls(
            name=data["name"],
            household_size=data.get("household_size", 1),
            notes=data.get("notes", ""),
            received_items=data.get("received_items", []),
        )

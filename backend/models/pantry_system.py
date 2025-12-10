# from .item import Item
# from .recipient import Recipient

# class PantrySystem:
#     def __init__(self):
#         self.items = []
#         self.recipients = []
#         self.history = []

#     def add_item(self, name, category, quantity):
#         for item in self.items:
#             if item.name.lower() == name.lower():
#                 item.update_quantity(quantity)
#                 return
#         new_item = Item(name, category, quantity)
#         self.items.append(new_item)

#     def update_item_quantity(self, name, amount):
#         for item in self.items:
#             if item.name.lower() == name.lower():
#                 item.update_quantity(amount)
#                 return True
#         return False

#     def add_recipient(self, name, household_size, notes=""):
#         new_recipient = Recipient(name, household_size, notes)
#         self.recipients.append(new_recipient)

#     def record_distribution(self, item_name, recipient_name, quantity):
#         item = next((i for i in self.items if i.name.lower() == item_name.lower()), None)
#         if not item:
#             return "Item not found."

#         if item.quantity < quantity:
#             return "Not enough stock."

#         recipient = next((r for r in self.recipients if r.name.lower() == recipient_name.lower()), None)
#         if not recipient:
#             return "Recipient not found."

#         item.update_quantity(-quantity)

#         self.history.append({
#             "item": item_name,
#             "recipient": recipient_name,
#             "quantity": quantity
#         })

#         return "SUCCESS"

#     def get_inventory(self):
#         return self.items

#     def get_low_stock(self, threshold):
#         return [item for item in self.items if item.quantity <= threshold]

# backend/models/pantry_system.py

# backend/models/pantry_system.py

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

from .item import Item
from .recipient import Recipient


class PantrySystem:
    """
    Core backend system for the food pantry.

    - Manages inventory (Items)
    - Manages recipients (Recipients)
    - Records distributions
    - Can save/load all data to/from a JSON file

    NOTE: This version is aligned with the Tkinter GUI in frontend/app.py.
    """

    def __init__(
        self, data_file: str = "pantry_data.json", auto_load: bool = True
    ) -> None:
        self.data_file = Path(data_file)

        # inventory: item name -> Item object
        self.inventory: Dict[str, Item] = {}

        # list of Recipient objects
        self.recipients: List[Recipient] = []

        # history of distributions (for GUI)
        # each entry: {"recipient", "item", "quantity", "timestamp"}
        self.history: List[Dict] = []

        if auto_load:
            self.load_data()

    # ---------- Properties for GUI ----------

    @property
    def items(self) -> List[Item]:
        """
        For GUI compatibility: returns a list of Item objects.
        Used by frontend/app.py when building item dropdowns.
        """
        return list(self.inventory.values())

    # ---------- Helper lookups ----------

    def get_item(self, name: str) -> Optional[Item]:
        """Return the Item with the given name, or None if not found."""
        return self.inventory.get(name)

    def get_recipient(self, name: str) -> Optional[Recipient]:
        """Return the Recipient with the given name, or None if not found."""
        for r in self.recipients:
            if r.name == name:
                return r
        return None

    # ---------- Inventory management ----------

    def add_item(self, name: str, category: str, quantity: int = 0) -> None:
        """
        Add a new item to the inventory, or increase quantity if it already exists.
        Called from the GUI "Add Donation / Item" screen.
        """
        if quantity < 0:
            raise ValueError("Initial quantity cannot be negative.")

        existing = self.get_item(name)
        if existing:
            existing.update_quantity(quantity)
        else:
            self.inventory[name] = Item(name=name, category=category, quantity=quantity)

    def update_item_quantity(self, name: str, amount: int) -> None:
        """
        Adjust the quantity of an item by the given amount.
        Positive to add, negative to remove.
        """
        item = self.get_item(name)
        if not item:
            raise KeyError(f"Item '{name}' not found in inventory.")
        item.update_quantity(amount)

    def get_inventory(self) -> List[Item]:
        """
        Return a list of Item objects for the GUI to display.
        frontend/app.py expects each item to have .name, .category, .quantity
        """
        return list(self.inventory.values())

    def get_low_stock_items(self, threshold: int = 5) -> List[Item]:
        """
        Return items with quantity <= threshold.
        Not directly used by the GUI, but useful for reports.
        """
        return [item for item in self.inventory.values() if item.quantity <= threshold]

    # ---------- Recipient management ----------

    def add_recipient(self, name: str, household_size: int, notes: str = "") -> None:
        """
        Add a new recipient if they don't already exist.
        Called from the GUI "Add Recipient" screen with notes.
        """
        if self.get_recipient(name) is not None:
            # Avoid duplicates quietly.
            return
        if household_size <= 0:
            raise ValueError("Household size must be positive.")
        self.recipients.append(
            Recipient(name=name, household_size=household_size, notes=notes)
        )

    def get_all_recipients(self) -> List[Dict]:
        """
        Return all recipients as dicts (not currently used by GUI, but handy).
        """
        return [r.to_dict() for r in self.recipients]

    # ---------- Distribution management ----------

    def record_distribution(
        self, item_name: str, recipient_name: str, quantity: int
    ) -> str:
        """
        Record that some quantity of an item was given to a recipient.

        This method is designed to match the GUI usage:
        - Returns "SUCCESS" on success
        - Returns an error message string on failure
        (instead of raising exceptions)
        """
        if quantity <= 0:
            return "Quantity must be positive."

        item = self.get_item(item_name)
        if not item:
            return f"Item '{item_name}' not found."

        recipient = self.get_recipient(recipient_name)
        if not recipient:
            return f"Recipient '{recipient_name}' not found."

        if item.quantity < quantity:
            return (
                f"Not enough '{item_name}' in stock. "
                f"Available: {item.quantity}, requested: {quantity}"
            )

        timestamp = datetime.now().isoformat(timespec="seconds")

        # Perform the distribution
        try:
            item.update_quantity(-quantity)
        except ValueError as e:
            return str(e)

        recipient.record_receipt(
            item_name=item_name, quantity=quantity, timestamp=timestamp
        )

        record = {
            "recipient": recipient_name,
            "item": item_name,
            "quantity": quantity,
            "timestamp": timestamp,
        }
        self.history.append(record)

        # Optionally auto-save on every distribution:
        self.save_data()

        return "SUCCESS"

    # ---------- Persistence (JSON save/load) ----------

    def save_data(self) -> None:
        """
        Save inventory, recipients, and history to a JSON file.
        """
        data = {
            "inventory": [item.to_dict() for item in self.inventory.values()],
            "recipients": [r.to_dict() for r in self.recipients],
            "history": self.history,
        }

        self.data_file.write_text(
            json.dumps(data, indent=2),
            encoding="utf-8",
        )

    def load_data(self) -> None:
        """
        Load inventory, recipients, and history from a JSON file, if it exists.
        If not, start with empty data.
        """
        if not self.data_file.exists():
            return

        raw = self.data_file.read_text(encoding="utf-8")
        if not raw.strip():
            return

        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            # Corrupted or invalid JSON; start fresh.
            return

        self.inventory.clear()
        self.recipients.clear()
        self.history.clear()

        for item_data in data.get("inventory", []):
            item = Item.from_dict(item_data)
            self.inventory[item.name] = item

        for rec_data in data.get("recipients", []):
            self.recipients.append(Recipient.from_dict(rec_data))

        self.history.extend(data.get("history", []))

from .item import Item
from .recipient import Recipient

class PantrySystem:
    def __init__(self):
        self.items = []
        self.recipients = []
        self.history = []

    def add_item(self, name, category, quantity):
        for item in self.items:
            if item.name.lower() == name.lower():
                item.update_quantity(quantity)
                return
        new_item = Item(name, category, quantity)
        self.items.append(new_item)

    def update_item_quantity(self, name, amount):
        for item in self.items:
            if item.name.lower() == name.lower():
                item.update_quantity(amount)
                return True
        return False

    def add_recipient(self, name, household_size, notes=""):
        new_recipient = Recipient(name, household_size, notes)
        self.recipients.append(new_recipient)

    def record_distribution(self, item_name, recipient_name, quantity):
        item = next((i for i in self.items if i.name.lower() == item_name.lower()), None)
        if not item:
            return "Item not found."

        if item.quantity < quantity:
            return "Not enough stock."

        recipient = next((r for r in self.recipients if r.name.lower() == recipient_name.lower()), None)
        if not recipient:
            return "Recipient not found."

        item.update_quantity(-quantity)

        self.history.append({
            "item": item_name,
            "recipient": recipient_name,
            "quantity": quantity
        })

        return "SUCCESS"

    def get_inventory(self):
        return self.items

    def get_low_stock(self, threshold):
        return [item for item in self.items if item.quantity <= threshold]

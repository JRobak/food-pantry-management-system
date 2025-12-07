class Item:
    def __init__(self, name, category, quantity):
        self.name = name
        self.category = category
        self.quantity = quantity

    def update_quantity(self, amount):
        self.quantity += amount

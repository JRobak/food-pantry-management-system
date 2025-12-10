# backend/main.py

from models.pantry_system import PantrySystem


def print_inventory(pantry: PantrySystem) -> None:
    print("\nCurrent Inventory:")
    for item in pantry.get_inventory():
        print(f"- {item.name} ({item.category}): {item.quantity}")


def print_history(pantry: PantrySystem) -> None:
    print("\nDistribution History:")
    if not pantry.history:
        print("  No distributions yet.")
        return
    for record in pantry.history:
        print(
            f"- {record.get('timestamp', '')}: "
            f"{record['recipient']} received {record['quantity']} of {record['item']}"
        )


def main() -> None:
    pantry = PantrySystem(data_file="pantry_data.json", auto_load=True)

    # If starting fresh, add a little sample data:
    if not pantry.inventory:
        pantry.add_item("Rice", "Grains", 50)
        pantry.add_item("Beans", "Canned Goods", 30)
        pantry.add_item("Pasta", "Grains", 10)

    if not pantry.recipients:
        pantry.add_recipient(
            "Alice Johnson", household_size=4, notes="Gluten-free preferred"
        )
        pantry.add_recipient("Marcus Smith", household_size=2, notes="")

    # Try a sample distribution:
    result = pantry.record_distribution("Rice", "Alice Johnson", 5)
    if result != "SUCCESS":
        print(f"[ERROR] {result}")

    print_inventory(pantry)
    print_history(pantry)


if __name__ == "__main__":
    main()

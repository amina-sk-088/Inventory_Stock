
import json
import os

# Matplotlib is optional
try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None


# Store inventory.json in the same folder as main.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_NAME = os.path.join(BASE_DIR, "inventory.json")


# ---------------- CLEAR SCREEN ----------------
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


# ---------------- LOAD INVENTORY ----------------
def load_inventory():
    if not os.path.exists(FILE_NAME):
        return {}

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            print("Invalid inventory file format.")
            return {}

        inventory = {}

        for product_id, product in data.items():
            if not isinstance(product, dict):
                continue

            try:
                price = float(product.get("price", 0))
                quantity = int(product.get("quantity", 0))
                low_limit = int(
                    product.get(
                        "low_limit",
                        product.get("low_stock_limit", 5)
                    )
                )

                if price < 0 or quantity < 0 or low_limit < 0:
                    continue

                inventory[str(product_id)] = {
                    "name": str(product.get("name", "Unknown")),
                    "price": price,
                    "quantity": quantity,
                    "low_limit": low_limit
                }

            except (TypeError, ValueError):
                continue

        return inventory

    except (json.JSONDecodeError, OSError) as error:
        print("Error loading inventory:", error)
        return {}


# ---------------- SAVE INVENTORY ----------------
def save_inventory(inventory):
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(inventory, file, indent=4)
        return True

    except OSError as error:
        print("Error saving inventory:", error)
        return False


# ---------------- INPUT VALIDATION ----------------
def get_number(message, number_type=float, minimum=0):
    while True:
        try:
            value = number_type(input(message).strip())

            if value < minimum:
                print("Please enter a valid number.")
                continue

            return value

        except ValueError:
            print("Invalid input. Please enter a valid number.")


# ---------------- 1. ADD PRODUCT ----------------
def add_product(inventory):
    print("\n========== ADD PRODUCT ==========")

    product_id = input("Enter product ID: ").strip()

    if not product_id:
        print("Product ID cannot be empty.")
        return

    if product_id in inventory:
        print("This product ID already exists.")
        return

    name = input("Enter product name: ").strip()

    if not name:
        print("Product name cannot be empty.")
        return

    price = get_number("Enter price: Rs. ", float)
    quantity = get_number("Enter quantity: ", int)
    low_limit = get_number("Enter low-stock limit: ", int)

    inventory[product_id] = {
        "name": name,
        "price": price,
        "quantity": quantity,
        "low_limit": low_limit
    }

    if save_inventory(inventory):
        print("\nProduct added successfully!")
        print("Product ID:", product_id)
        print("Product name:", name)
        print("Price: Rs.", round(price, 2))
        print("Available quantity:", quantity)
        print("Low-stock limit:", low_limit)
    else:
        del inventory[product_id]


# ---------------- 2. VIEW PRODUCTS ----------------
def view_products(inventory):
    print("\n========== VIEW PRODUCTS ==========")

    if not inventory:
        print("No products available.")
        return

    for product_id, product in inventory.items():
        print("\nProduct ID:", product_id)
        print("Name:", product["name"])
        print("Price: Rs.", round(product["price"], 2))
        print("Available quantity:", product["quantity"])
        print("Low-stock limit:", product["low_limit"])
        print("-----------------------------------")

    print("\nTotal number of products:", len(inventory))


# ---------------- 3. SELL PRODUCT ----------------
def sell_product(inventory):
    print("\n========== SELL PRODUCT ==========")

    product_id = input("Enter product ID: ").strip()

    if product_id not in inventory:
        print("Product not found. Check the product ID.")
        return

    product = inventory[product_id]

    print("Product:", product["name"])
    print("Available stock:", product["quantity"])

    if product["quantity"] == 0:
        print("This product is out of stock.")
        return

    quantity = get_number("Enter quantity to sell: ", int, 1)

    if quantity > product["quantity"]:
        print("Insufficient stock!")
        print("Available quantity:", product["quantity"])
        return

    old_quantity = product["quantity"]
    product["quantity"] -= quantity

    if save_inventory(inventory):
        print("\nSale completed successfully!")
        print("Quantity sold:", quantity)
        print("Remaining stock:", product["quantity"])
        print(
            "Sale value: Rs.",
            round(product["price"] * quantity, 2)
        )
    else:
        product["quantity"] = old_quantity


# ---------------- 4. RESTOCK PRODUCT ----------------
def restock_product(inventory):
    print("\n========== RESTOCK PRODUCT ==========")

    product_id = input("Enter product ID: ").strip()

    if product_id not in inventory:
        print("Product not found. Check the product ID.")
        return

    product = inventory[product_id]

    print("Product:", product["name"])
    print("Current stock:", product["quantity"])

    quantity = get_number("Enter quantity to add: ", int, 1)

    old_quantity = product["quantity"]
    product["quantity"] += quantity

    if save_inventory(inventory):
        print("\nStock updated successfully!")
        print("New available quantity:", product["quantity"])
    else:
        product["quantity"] = old_quantity


# ---------------- 5. LOW STOCK ALERTS ----------------
def low_stock_alert(inventory):
    print("\n========== LOW STOCK ALERTS ==========")

    if not inventory:
        print("No products available.")
        return

    found = False

    for product_id, product in inventory.items():
        quantity = product["quantity"]
        limit = product["low_limit"]

        if quantity == 0:
            print(
                "OUT OF STOCK:",
                product["name"],
                "| Available: 0",
                "| Low-stock limit:", limit
            )
            found = True

        elif quantity <= limit:
            print(
                "LOW STOCK:",
                product["name"],
                "| Available:", quantity,
                "| Low-stock limit:", limit
            )
            found = True

    if not found:
        print("All products have sufficient stock.")

    print("\nLow-stock check completed.")


# ---------------- 6. TOTAL INVENTORY VALUE ----------------
def total_inventory_value(inventory):
    print("\n========== TOTAL INVENTORY VALUE ==========")

    if not inventory:
        print("No products available.")
        print("Total Inventory Value: Rs. 0.00")
        return

    total = 0

    for product in inventory.values():
        value = product["price"] * product["quantity"]
        total += value

        print(
            product["name"],
            "-",
            product["quantity"],
            "units x Rs.",
            product["price"],
            "= Rs.",
            round(value, 2)
        )

    print("-----------------------------------")
    print("TOTAL INVENTORY VALUE: Rs.", round(total, 2))


# ---------------- 7. VIEW CHARTS ----------------
def display_charts(inventory):
    print("\n========== INVENTORY CHARTS ==========")

    if not inventory:
        print("No products available. Add products first.")
        return

    if plt is None:
        print("Matplotlib is not installed.")
        print("Run: python -m pip install matplotlib")
        return

    names = [p["name"] for p in inventory.values()]
    quantities = [p["quantity"] for p in inventory.values()]
    values = [
        p["price"] * p["quantity"]
        for p in inventory.values()
    ]
    limits = [p["low_limit"] for p in inventory.values()]

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle("Inventory Management Dashboard")

    # Chart 1: Available stock
    axes[0, 0].bar(names, quantities)
    axes[0, 0].set_title("Available Stock")
    axes[0, 0].set_ylabel("Quantity")

    # Chart 2: Inventory value
    axes[0, 1].bar(names, values)
    axes[0, 1].set_title("Inventory Value")
    axes[0, 1].set_ylabel("Value in Rs.")

    # Chart 3: Stock distribution
    if sum(quantities) > 0:
        axes[1, 0].pie(
            quantities,
            labels=names,
            autopct="%1.1f%%"
        )
    else:
        axes[1, 0].text(
            0.5, 0.5,
            "No stock available",
            ha="center",
            va="center"
        )

    axes[1, 0].set_title("Stock Distribution")

    # Chart 4: Stock versus low-stock limit
    axes[1, 1].plot(
        names,
        quantities,
        marker="o",
        label="Current Stock"
    )
    axes[1, 1].plot(
        names,
        limits,
        marker="x",
        label="Low-stock Limit"
    )
    axes[1, 1].set_title("Stock vs Low-stock Limit")
    axes[1, 1].legend()

    for axis in axes.flat:
        axis.tick_params(axis="x", rotation=30)

    plt.tight_layout()
    plt.show()
    plt.close(fig)


# ---------------- MAIN MENU ----------------
def main():
    inventory = load_inventory()

    while True:
        clear_screen()

        print("\n===================================")
        print(" INVENTORY AND STOCK MANAGEMENT")
        print("===================================")
        print("1. Add Product")
        print("2. View Products")
        print("3. Sell Product")
        print("4. Restock Product")
        print("5. Low Stock Alerts")
        print("6. Total Inventory Value")
        print("7. View Charts")
        print("8. Exit")
        print("===================================")

        choice = input("Enter your choice (1-8): ").strip()

        if choice == "8":
            clear_screen()
            print("Thank you for using the system!")
            break

        # Clear the menu before displaying the selected operation
        clear_screen()

        if choice == "1":
            add_product(inventory)

        elif choice == "2":
            view_products(inventory)

        elif choice == "3":
            sell_product(inventory)

        elif choice == "4":
            restock_product(inventory)

        elif choice == "5":
            low_stock_alert(inventory)

        elif choice == "6":
            total_inventory_value(inventory)

        elif choice == "7":
            display_charts(inventory)

        else:
            print("Invalid choice. Please enter a number from 1 to 8.")

        input("\nPress Enter to return to the menu...")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram stopped.")

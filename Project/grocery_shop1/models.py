#models.py file

import json
from dataclasses import dataclass, asdict, field
from pathlib import Path

INVENTORY_FILE = Path("inventory.json")


@dataclass
class Product:
    name: str
    price: float
    stock: float


class Inventory:
    def __init__(self):
        self._products: dict[str, Product] = {}
        self.load()  # Load inventory from JSON if exists

    def _key(self, name: str) -> str:
        return name.strip().lower()

    def add_or_update(self, name: str, price: float, stock_delta: float) -> str:
        k = self._key(name)
        if k in self._products:
            p = self._products[k]
            p.stock += stock_delta
            p.price = price
            self.save()
            return f"Updated {p.name}: stock={p.stock}, price={p.price}"
        else:
            self._products[k] = Product(name=name.strip(), price=price, stock=stock_delta)
            self.save()
            return f"Added new product {name.strip()} with stock={stock_delta}, price={price}"

    def find(self, name: str) -> Product | None:
        return self._products.get(self._key(name))

    def list_all(self) -> list[Product]:
        return list(self._products.values())

    def reduce_stock(self, name: str, qty: float) -> tuple[bool, str]:
        p = self.find(name)
        if p is None:
            return False, f"{name} not found in inventory."
        if qty <= 0:
            return False, "Quantity must be > 0."
        if p.stock < qty:
            return False, f"Not enough stock for {p.name}. Available: {p.stock}"
        p.stock -= qty
        self.save()
        return True, f"Reserved {qty} of {p.name}."

    def restore_stock(self, name: str, qty: float) -> None:
        p = self.find(name)
        if p and qty > 0:
            p.stock += qty
            self.save()

    # ---------- JSON Persistence ----------
    def save(self):
        data = [asdict(p) for p in self._products.values()]
        with open(INVENTORY_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def load(self):
        if INVENTORY_FILE.exists():
            with open(INVENTORY_FILE, "r") as f:
                data = json.load(f)
                for item in data:
                    self._products[self._key(item["name"])] = Product(**item)


class Bill:
    def __init__(self, inventory: Inventory):
        self.inventory = inventory
        self.cart: dict[str, dict] = {}
        self.discount_percent: float = 0.0

    def _key(self, name: str) -> str:
        return name.strip().lower()

    def add_to_cart(self, name: str, qty: float) -> tuple[bool, str]:
        ok, msg = self.inventory.reduce_stock(name, qty)
        if not ok:
            return False, msg
        k = self._key(name)
        prod = self.inventory.find(name)
        price = prod.price if prod else 0.0
        if k in self.cart:
            self.cart[k]["qty"] += qty
            self.cart[k]["price"] = price
        else:
            self.cart[k] = {"name": prod.name if prod else name.strip(), "price": price, "qty": qty}
        return True, f"Added {qty} x {self.cart[k]['name']} to cart."

    def remove_from_cart(self, name: str) -> tuple[bool, str]:
        k = self._key(name)
        if k not in self.cart:
            return False, f"{name} not found in cart."
        item = self.cart.pop(k)
        self.inventory.restore_stock(item["name"], item["qty"])
        return True, f"Removed {item['name']} from cart."

    def apply_discount(self, percent: float) -> tuple[bool, str]:
        if percent < 0 or percent > 100:
            return False, "Discount must be between 0 and 100."
        self.discount_percent = percent
        return True, f"Discount of {percent}% applied."

    def clear_discount(self):
        self.discount_percent = 0.0

    def subtotal(self) -> float:
        return sum(v["price"] * v["qty"] for v in self.cart.values())

    def totals(self) -> dict:
        sub = self.subtotal()
        discount_amt = (self.discount_percent / 100.0) * sub if self.discount_percent > 0 else 0.0
        final_total = sub - discount_amt
        return {
            "subtotal": round(sub, 2),
            "discount_percent": self.discount_percent,
            "discount_amount": round(discount_amt, 2),
            "final_total": round(final_total, 2),
        }

    def checkout(self) -> dict:
        summary = {"items": list(self.cart.values()), "totals": self.totals()}
        self.cart.clear()
        self.clear_discount()
        return summary
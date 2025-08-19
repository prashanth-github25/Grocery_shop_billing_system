#main.py file

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from models import Inventory, Bill

app = FastAPI()

# Static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Global state (in-memory)
inventory = Inventory()
bill = Bill(inventory)

# Preload items if inventory is empty
if not inventory.list_all():
    inventory.add_or_update("Rice", 55, 30)
    inventory.add_or_update("Sugar", 42, 20)
    inventory.add_or_update("Milk", 30, 25)
    inventory.add_or_update("Oil", 125, 12)


def redirect(url: str, msg: str | None = None):
    if msg:
        return RedirectResponse(url=f"{url}?msg={msg}", status_code=303)
    return RedirectResponse(url=url, status_code=303)


@app.get("/", response_class=HTMLResponse)
def home(request: Request, msg: str | None = None):
    return templates.TemplateResponse("index.html", {"request": request, "msg": msg})


# ---------------- Inventory ----------------
@app.get("/inventory", response_class=HTMLResponse)
def get_inventory(request: Request, msg: str | None = None):
    products = inventory.list_all()
    return templates.TemplateResponse(
        "inventory.html", {"request": request, "products": products, "msg": msg}
    )


@app.post("/inventory/add-update")
def add_update_product(name: str = Form(...), price: float = Form(...), stock: float = Form(...)):
    message = inventory.add_or_update(name, price, stock)
    return redirect("/inventory", message)


# ---------------- Billing / Cart ----------------
@app.get("/billing", response_class=HTMLResponse)
def billing_page(request: Request, msg: str | None = None):
    products = inventory.list_all()
    cart_items = list(bill.cart.values())
    totals = bill.totals()
    return templates.TemplateResponse(
        "billing.html",
        {
            "request": request,
            "products": products,
            "cart_items": cart_items,
            "totals": totals,
            "msg": msg,
        },
    )


@app.post("/cart/add")
def add_to_cart(product_name: str = Form(...), quantity: float = Form(...)):
    ok, message = bill.add_to_cart(product_name, quantity)
    return redirect("/billing", message)


@app.post("/cart/remove")
def remove_from_cart(product_name: str = Form(...)):
    ok, message = bill.remove_from_cart(product_name)
    return redirect("/billing", message)


@app.post("/discount/apply")
def apply_discount(percent: float = Form(...)):
    ok, message = bill.apply_discount(percent)
    return redirect("/billing", message)


@app.post("/checkout")
def checkout():
    _ = bill.checkout()
    return redirect("/", "Checkout complete. Cart cleared.")


# ---------------- CLI Inventory Display ----------------
def show_inventory_cli():
    print("\n--- Current Inventory ---")
    products = inventory.list_all()
    if not products:
        print("Inventory is empty.")
    else:
        for product in products:
            print(f"{product.name} - Price: ₹{product.price} - Stock: {product.stock}")


if __name__ == "__main__":
    while True:
        print("\nCommands:")
        print("1. Show Inventory")
        print("2. Exit")
        choice = input("Enter choice: ").strip()
        if choice == "1":
            show_inventory_cli()
        elif choice == "2":
            break
        else:
            print("Invalid choice.")

import json
from datetime import date
from urllib.parse import quote

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Order, Product, SiteSettings

DEFAULT_PRODUCTS = [
    {"name": "Fresh Oyster Mushrooms", "weight": "250 g", "price": 50,
     "description": "A handy pack for curries, stir-fries and everyday cooking."},
    {"name": "Fresh Oyster Mushrooms", "weight": "500 g", "price": 95,
     "description": "A family-size pack for generous meals and sharing."},
    {"name": "Fresh Oyster Mushrooms", "weight": "1 kg", "price": 180,
     "description": "A bulk-friendly pack for restaurants, shops and big cooks."},
]

def seed_products():
    if not Product.objects.exists():
        Product.objects.bulk_create([Product(**item) for item in DEFAULT_PRODUCTS])

def home(request):
    seed_products()
    products = Product.objects.all().order_by("price")
    return render(request, "store/home.html", {"products": products})

def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Your customer account has been created.")
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "store/register.html", {"form": form})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "store/my_orders.html", {"orders": orders})

@login_required
@require_POST
def place_order(request):
    seed_products()
    try:
        raw_items = json.loads(request.POST.get("items", "[]"))
    except (json.JSONDecodeError, TypeError):
        messages.error(request, "Your basket could not be read. Please try again.")
        return redirect("home")
    if not isinstance(raw_items, list) or not raw_items:
        messages.error(request, "Please add at least one mushroom pack.")
        return redirect("home")

    items, total = [], 0
    valid_products = {str(p.id): p for p in Product.objects.filter(available=True)}
    for entry in raw_items:
        if not isinstance(entry, dict):
            continue
        product = valid_products.get(str(entry.get("id", "")))
        try:
            qty = int(entry.get("quantity", 0))
        except (TypeError, ValueError):
            qty = 0
        if product and 1 <= qty <= 99:
            subtotal = product.price * qty
            total += subtotal
            items.append({"id": product.id, "name": product.name, "weight": product.weight,
                          "price": product.price, "quantity": qty, "subtotal": subtotal})
    if not items:
        messages.error(request, "Please choose valid product quantities.")
        return redirect("home")

    name = request.POST.get("customer_name", "").strip()[:120]
    phone = request.POST.get("phone", "").strip()[:20]
    address = request.POST.get("address", "").strip()[:2000]
    area = request.POST.get("area", "").strip()[:120]
    payment = request.POST.get("payment_method", "cod")
    notes = request.POST.get("notes", "").strip()[:2000]
    raw_date = request.POST.get("preferred_date", "").strip()
    if not name or not phone or not address:
        messages.error(request, "Please fill in your name, phone number and delivery address.")
        return redirect("home")
    if payment not in ("cod", "upi"):
        payment = "cod"
    try:
        preferred_date = date.fromisoformat(raw_date) if raw_date else None
    except ValueError:
        preferred_date = None

    order = Order.objects.create(user=request.user, customer_name=name, phone=phone, address=address,
        area=area, preferred_date=preferred_date, payment_method=payment, notes=notes,
        items_json=items, total=total)
    site = SiteSettings.current()
    whatsapp_number = "".join(c for c in (site.whatsapp_number or "") if c.isdigit())
    lines = [f"Hi {site.business_name}! I'd like to place order #{order.id}.", "", "ORDER ITEMS:"]
    for item in items:
        lines.append(f"- {item['name']} ({item['weight']}) x {item['quantity']} = Rs {item['subtotal']}")
    lines += ["", f"Estimated product total: Rs {total}",
        "(Please confirm stock, final price and delivery charges.)", "", "CUSTOMER DETAILS:",
        f"Name: {name}", f"Phone: {phone}", f"Address: {address}", f"Area: {area or 'Not specified'}",
        f"Preferred date: {preferred_date.isoformat() if preferred_date else 'Flexible'}",
        f"Payment: {'Cash on delivery' if payment == 'cod' else 'UPI (confirm details in chat)'}",
        f"Notes: {notes or 'None'}", "", "Please confirm my order and delivery slot."]
    whatsapp_url = f"https://wa.me/{whatsapp_number}?text={quote(chr(10).join(lines))}"
    return render(request, "store/order_confirmation.html", {"order": order, "whatsapp_url": whatsapp_url})

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    site = SiteSettings.current()
    whatsapp_number = "".join(c for c in (site.whatsapp_number or "") if c.isdigit())
    lines = [f"Hi {site.business_name}! Checking on order #{order.id}.",
             f"Name: {order.customer_name}", f"Total: Rs {order.total}"]
    return render(request, "store/order_confirmation.html", {
        "order": order, "whatsapp_url": f"https://wa.me/{whatsapp_number}?text={quote(chr(10).join(lines))}",
    })

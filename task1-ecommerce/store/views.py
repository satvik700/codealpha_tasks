from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .models import Product, Order, OrderItem

def product_list(request):
    q = request.GET.get("q", "")
    products = Product.objects.filter(name__icontains=q)
    return render(request, "store/list.html", {"products": products, "q": q})

def product_detail(request, pk):
    return render(request, "store/detail.html", {"p": get_object_or_404(Product, pk=pk)})

def _lines(request):
    items, total = [], Decimal(0)
    for pid, qty in request.session.get("cart", {}).items():
        p = Product.objects.filter(pk=pid).first()
        if p:
            sub = p.price * qty; total += sub
            items.append({"p": p, "qty": qty, "sub": sub})
    return items, total

def cart(request):
    items, total = _lines(request)
    return render(request, "store/cart.html", {"items": items, "total": total})

@require_POST
def cart_add(request, pk):
    p = get_object_or_404(Product, pk=pk)
    c = request.session.get("cart", {})
    qty = min(int(request.POST.get("qty", 1) or 1), p.stock)
    c[str(pk)] = min(c.get(str(pk), 0) + max(qty, 1), p.stock)
    request.session["cart"] = c
    messages.success(request, f"Added {p.name} to your cart.")
    return redirect(request.POST.get("next") or "cart")

@require_POST
def cart_update(request, pk):
    c = request.session.get("cart", {})
    qty = int(request.POST.get("qty", 0) or 0)
    if qty <= 0: c.pop(str(pk), None)
    else: c[str(pk)] = min(qty, get_object_or_404(Product, pk=pk).stock)
    request.session["cart"] = c
    return redirect("cart")

@login_required
def checkout(request):
    items, total = _lines(request)
    if not items:
        return redirect("cart")
    if request.method == "POST":
        with transaction.atomic():
            order = Order.objects.create(user=request.user, name=request.POST["name"],
                                         address=request.POST["address"], total=total)
            for i in items:
                OrderItem.objects.create(order=order, product=i["p"], quantity=i["qty"], price=i["p"].price)
                i["p"].stock = max(i["p"].stock - i["qty"], 0); i["p"].save()
        request.session["cart"] = {}
        messages.success(request, f"Order #{order.id} placed. Thank you!")
        return redirect("orders")
    return render(request, "store/checkout.html", {"items": items, "total": total})

@login_required
def orders(request):
    return render(request, "store/orders.html", {"orders": request.user.orders.prefetch_related("items__product")})

def register(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        login(request, form.save()); return redirect("product_list")
    return render(request, "registration/register.html", {"form": form})

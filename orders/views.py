from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from menu.models import MenuItem

from .forms import OrderStatusForm
from .models import Order, OrderItem


@login_required
def order_create(request):
    menu_items = MenuItem.objects.filter(is_available=True)

    if request.method == "POST":
        order_lines = []

        # Format: quantity_{item_id}=N
        for item in menu_items:
            raw = request.POST.get(f"quantity_{item.pk}", "").strip()
            if raw:
                try:
                    qty = int(raw)
                except ValueError:
                    continue
                if 1 <= qty <= 99:
                    order_lines.append((item, qty))

        # Fallback format: items as "item_id:quantity" pairs
        if not order_lines:
            for pair in request.POST.getlist("items"):
                try:
                    item_id, qty = pair.split(":")
                    item_id = int(item_id)
                    qty = int(qty)
                except (ValueError, AttributeError):
                    continue
                if qty < 1 or qty > 99:
                    continue
                try:
                    item = menu_items.get(pk=item_id)
                except MenuItem.DoesNotExist:
                    continue
                order_lines.append((item, qty))

        if not order_lines:
            messages.error(request, "Please select at least one item before placing an order.")
            return render(request, "orders/order_create.html", {"menu_items": menu_items})

        order = Order.objects.create(customer=request.user)
        OrderItem.objects.bulk_create(
            [OrderItem(order=order, menu_item=item, quantity=qty) for item, qty in order_lines]
        )
        messages.success(request, "Order placed successfully!")
        return redirect("order-history")

    return render(request, "orders/order_create.html", {"menu_items": menu_items})


@login_required
def order_history(request):
    if request.user.is_staff:
        orders = (
            Order.objects.select_related("customer")
            .prefetch_related("items__menu_item")
            .order_by("-created_at")
        )
    else:
        orders = (
            Order.objects.filter(customer=request.user)
            .select_related("customer")
            .prefetch_related("items__menu_item")
            .order_by("-created_at")
        )
    return render(request, "orders/order_history.html", {"orders": orders})


@login_required
def order_detail(request, pk):
    if request.user.is_staff:
        order = get_object_or_404(
            Order.objects.select_related("customer").prefetch_related("items__menu_item"),
            pk=pk,
        )
    else:
        order = get_object_or_404(
            Order.objects.select_related("customer").prefetch_related("items__menu_item"),
            pk=pk,
            customer=request.user,
        )
    return render(request, "orders/order_detail.html", {"order": order})


@login_required
def order_cancel(request, order_id):
    if request.method != "POST":
        return redirect("order-history")

    order = get_object_or_404(Order, pk=order_id)

    if order.status != Order.Status.PENDING:
        messages.error(request, "Only pending orders can be cancelled.")
        return redirect("order-history")

    if order.customer != request.user and not request.user.is_staff:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("You are not allowed to cancel this order.")

    order.status = Order.Status.CANCELLED
    order.save()
    messages.success(request, "Order cancelled successfully.")
    return redirect("order-history")


@login_required
@staff_member_required
def order_delete(request, order_id):
    if request.method != "POST":
        return redirect("order-history")

    order = get_object_or_404(Order, pk=order_id)

    if order.status != Order.Status.CANCELLED:
        messages.error(request, "Only cancelled orders can be deleted.")
        return redirect("order-history")

    order.delete()
    messages.success(request, "Order deleted.")
    return redirect("order-history")


@login_required
@staff_member_required
def order_manage(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == "POST":
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, "Order status updated.")
            return redirect("order-history")
    else:
        form = OrderStatusForm(instance=order)
    return render(request, "orders/order_manage.html", {"order": order, "form": form})

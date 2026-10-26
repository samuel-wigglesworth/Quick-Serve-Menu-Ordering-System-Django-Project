from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from .forms import OrderCreateForm, OrderStatusForm
from .models import Order, OrderItem


def staff_required(view_func):
    return user_passes_test(lambda user: user.is_staff, login_url="dashboard")(view_func)


@login_required
def order_create(request):
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(customer=request.user)
            OrderItem.objects.create(
                order=order,
                menu_item=form.cleaned_data["menu_item"],
                quantity=form.cleaned_data["quantity"],
            )
            return redirect("order-history")
    else:
        form = OrderCreateForm()
    return render(request, "orders/order_create.html", {"form": form})


@login_required
def order_history(request):
    if request.user.is_staff:
        orders = Order.objects.select_related("customer").prefetch_related("items__menu_item").order_by("-created_at")
    else:
        orders = (
            Order.objects.filter(customer=request.user)
            .select_related("customer")
            .prefetch_related("items__menu_item")
            .order_by("-created_at")
        )
    return render(request, "orders/order_history.html", {"orders": orders})


@staff_required
def order_manage(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == "POST":
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect("order-history")
    else:
        form = OrderStatusForm(instance=order)
    return render(request, "orders/order_manage.html", {"order": order, "form": form})

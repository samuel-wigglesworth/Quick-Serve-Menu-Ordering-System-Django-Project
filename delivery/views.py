from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from orders.models import Order

from .forms import DeliveryStatusForm
from .models import DeliveryStatus


@login_required
def delivery_track(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if not request.user.is_staff and order.customer != request.user:
        return redirect("order-history")

    # Gracefully handle orders that don't have a delivery status yet
    try:
        status = order.delivery_status
    except DeliveryStatus.DoesNotExist:
        status = None

    return render(request, "delivery/track.html", {"order": order, "status": status})


@login_required
@staff_member_required
def delivery_update(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    status, _ = DeliveryStatus.objects.get_or_create(order=order)
    if request.method == "POST":
        form = DeliveryStatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            return redirect("delivery-track", order_id=order.pk)
    else:
        form = DeliveryStatusForm(instance=status)
    return render(request, "delivery/update.html", {"order": order, "form": form})


@login_required
@staff_member_required
def delivery_list(request):
    deliveries = (
        DeliveryStatus.objects
        .select_related("order", "order__customer")
        .order_by("-updated_at")
    )
    return render(request, "delivery/list.html", {"deliveries": deliveries})


@login_required
@staff_member_required
def delivery_create(request):
    # Only show orders that don't have a delivery status yet
    orders_without_delivery = Order.objects.exclude(
        pk__in=DeliveryStatus.objects.values_list("order_id", flat=True)
    ).select_related("customer").order_by("-created_at")

    if request.method == "POST":
        order_id = request.POST.get("order")
        order = get_object_or_404(Order, pk=order_id)
        # Prevent duplicate delivery status
        delivery_status, created = DeliveryStatus.objects.get_or_create(order=order)
        if created:
            form = DeliveryStatusForm(request.POST, instance=delivery_status)
            if form.is_valid():
                form.save()
            messages.success(request, "Delivery record created successfully.")
        else:
            messages.warning(request, "A delivery record already exists for this order.")
        return redirect("delivery-list")

    return render(
        request,
        "delivery/create.html",
        {"orders": orders_without_delivery},
    )


@login_required
@staff_member_required
def delivery_delete(request, status_id):
    if request.method == "POST":
        delivery = get_object_or_404(DeliveryStatus, pk=status_id)
        delivery.delete()
        messages.success(request, "Delivery record deleted.")
    return redirect("delivery-list")

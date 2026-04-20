from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from orders.models import Order

from .forms import DeliveryStatusForm
from .models import DeliveryStatus


def staff_required(view_func):
    return user_passes_test(lambda user: user.is_staff, login_url="dashboard")(view_func)


@login_required
def delivery_track(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if not request.user.is_staff and order.customer != request.user:
        return redirect("order-history")

    status, _ = DeliveryStatus.objects.get_or_create(order=order)
    return render(request, "delivery/track.html", {"order": order, "status": status})


@staff_required
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

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render

from orders.models import Order

from .forms import CustomerEditForm, CustomerProfileForm
from .models import CustomerProfile

User = get_user_model()


@login_required
def profile_view(request):
    profile, _ = CustomerProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = CustomerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("customer-profile")
    else:
        form = CustomerProfileForm(instance=profile)

    recent_orders = (
        Order.objects.filter(customer=request.user)
        .prefetch_related("items__menu_item")
        .order_by("-created_at")[:5]
    )

    return render(request, "customers/profile.html", {
        "form": form,
        "profile": profile,
        "recent_orders": recent_orders,
    })


@login_required
@staff_member_required
def customer_list(request):
    profiles = CustomerProfile.objects.select_related("user").all()
    return render(request, "customers/customer_list.html", {"profiles": profiles})


@login_required
@staff_member_required
def customer_edit(request, pk):
    profile = get_object_or_404(CustomerProfile, pk=pk)
    if request.method == "POST":
        form = CustomerEditForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer updated successfully")
            return redirect("customer-list")
    else:
        form = CustomerEditForm(instance=profile)
    return render(request, "customers/customer_edit.html", {"form": form, "profile": profile})


@login_required
@staff_member_required
def customer_delete(request, pk):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    profile = get_object_or_404(CustomerProfile, pk=pk)
    active_statuses_excluded = ["cancelled", "delivered"]
    has_active_orders = Order.objects.filter(customer=profile.user).exclude(
        status__in=active_statuses_excluded
    ).exists()

    if has_active_orders:
        messages.error(request, "Cannot delete — customer has active orders")
        return redirect("customer-list")

    user = profile.user
    profile.delete()
    user.delete()
    messages.success(request, "Customer deleted")
    return redirect("customer-list")

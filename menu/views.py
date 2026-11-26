from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db.models.deletion import ProtectedError
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render

from .forms import MenuItemForm
from .models import MenuItem


def menu_list(request):
    """Public menu — no login required so anyone can browse."""
    items = MenuItem.objects.filter(is_available=True).order_by("name")
    return render(request, "menu/menu_list.html", {"items": items})


@login_required
@staff_member_required
def menu_manage(request):
    items = MenuItem.objects.order_by("name")
    return render(request, "menu/menu_manage.html", {"items": items})


@login_required
@staff_member_required
def menu_add(request):
    if request.method == "POST":
        form = MenuItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Menu item added successfully.")
            return redirect("menu-manage")
    else:
        form = MenuItemForm()
    return render(request, "menu/menu_add.html", {"form": form})


@login_required
@staff_member_required
def menu_edit(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == "POST":
        form = MenuItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Menu item updated successfully.")
            return redirect("menu-manage")
    else:
        form = MenuItemForm(instance=item)
    return render(request, "menu/menu_edit.html", {"form": form, "item": item})


@login_required
@staff_member_required
def menu_delete(request, pk):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    item = get_object_or_404(MenuItem, pk=pk)
    # orderitem_set uses the default related_name; items is the custom one
    if item.items.exists():
        messages.error(request, "Cannot delete — this item has existing orders.")
        return redirect("menu-manage")
    try:
        item.delete()
        messages.success(request, "Menu item deleted.")
    except ProtectedError:
        messages.error(request, "Cannot delete — this item has existing orders.")
    return redirect("menu-manage")

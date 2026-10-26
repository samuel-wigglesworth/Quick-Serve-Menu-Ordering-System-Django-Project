from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render

from .forms import MenuItemForm
from .models import MenuItem


def staff_required(view_func):
    return user_passes_test(lambda user: user.is_staff, login_url="dashboard")(view_func)


@login_required
def menu_list(request):
    items = MenuItem.objects.filter(is_available=True).order_by("name")
    return render(request, "menu/menu_list.html", {"items": items})


@staff_required
def menu_manage(request):
    if request.method == "POST":
        form = MenuItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("menu-manage")
    else:
        form = MenuItemForm()

    items = MenuItem.objects.order_by("name")
    return render(request, "menu/menu_manage.html", {"form": form, "items": items})

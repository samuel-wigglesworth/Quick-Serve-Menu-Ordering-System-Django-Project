from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum
from django.shortcuts import render

from orders.models import Order, OrderItem


def staff_required(view_func):
    return user_passes_test(lambda user: user.is_staff, login_url="dashboard")(view_func)


@staff_required
def sales_report(request):
    orders = Order.objects.all()
    total_orders = orders.count()
    delivered_orders = orders.filter(status=Order.Status.DELIVERED).count()

    top_items = (
        OrderItem.objects.values("menu_item__name")
        .annotate(total_quantity=Sum("quantity"))
        .order_by("-total_quantity")[:5]
    )

    context = {
        "total_orders": total_orders,
        "delivered_orders": delivered_orders,
        "top_items": top_items,
    }
    return render(request, "reports/sales_report.html", context)

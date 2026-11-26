import json
from datetime import timedelta

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, DecimalField, ExpressionWrapper, F, Sum
from django.shortcuts import render
from django.utils import timezone

from customers.models import CustomerProfile
from orders.models import Order, OrderItem


# ---------------------------------------------------------------------------
# Existing sales report (kept intact)
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# New analytics dashboard view
# ---------------------------------------------------------------------------

@login_required
@staff_member_required
def reports_view(request):
    # ------------------------------------------------------------------
    # 1. Top 10 menu items by order quantity (bar chart)
    # ------------------------------------------------------------------
    top_items = (
        OrderItem.objects.values("menu_item__name")
        .annotate(total_qty=Sum("quantity"))
        .order_by("-total_qty")[:10]
    )
    bar_labels = [item["menu_item__name"] for item in top_items]
    bar_data = [item["total_qty"] for item in top_items]

    # ------------------------------------------------------------------
    # 2. Order status breakdown (doughnut chart)
    # ------------------------------------------------------------------
    status_counts = Order.objects.values("status").annotate(count=Count("id"))
    doughnut_labels = [s["status"] for s in status_counts]
    doughnut_data = [s["count"] for s in status_counts]

    # ------------------------------------------------------------------
    # 3. Orders per day — last 30 days (line chart)
    # ------------------------------------------------------------------
    thirty_days_ago = timezone.now().date() - timedelta(days=29)
    daily = (
        Order.objects.filter(created_at__date__gte=thirty_days_ago)
        .extra({"day": "date(created_at)"})
        .values("day")
        .annotate(count=Count("id"))
        .order_by("day")
    )
    line_labels = [entry["day"] for entry in daily]
    line_data = [entry["count"] for entry in daily]

    # ------------------------------------------------------------------
    # 4. KPI cards
    # ------------------------------------------------------------------
    total_orders = Order.objects.count()

    # total_amount is a Python property, not a DB column.
    # Compute delivered revenue via OrderItem aggregation (quantity × price).
    delivered_revenue_agg = (
        OrderItem.objects.filter(order__status="delivered")
        .aggregate(
            total=Sum(
                ExpressionWrapper(
                    F("quantity") * F("menu_item__price"),
                    output_field=DecimalField(),
                )
            )
        )
    )
    total_revenue = delivered_revenue_agg["total"] or 0

    total_customers = CustomerProfile.objects.count()
    pending_orders = Order.objects.filter(status="pending").count()

    # ------------------------------------------------------------------
    # Serialise for Chart.js
    # ------------------------------------------------------------------
    context = {
        "bar_labels_json": json.dumps(bar_labels, cls=DjangoJSONEncoder),
        "bar_data_json": json.dumps(bar_data, cls=DjangoJSONEncoder),
        "doughnut_labels_json": json.dumps(doughnut_labels, cls=DjangoJSONEncoder),
        "doughnut_data_json": json.dumps(doughnut_data, cls=DjangoJSONEncoder),
        "line_labels_json": json.dumps(line_labels, cls=DjangoJSONEncoder),
        "line_data_json": json.dumps(line_data, cls=DjangoJSONEncoder),
        # KPI cards (plain Python values, not JSON)
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "total_customers": total_customers,
        "pending_orders": pending_orders,
    }
    return render(request, "reports/reports.html", context)

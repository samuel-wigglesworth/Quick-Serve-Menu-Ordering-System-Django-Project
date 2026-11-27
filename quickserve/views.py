import json
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import redirect, render
from django.utils import timezone

from customers.models import CustomerProfile
from menu.models import MenuItem
from orders.models import Order


@login_required
def dashboard(request):
    # Non-staff users (customers) should not see the dashboard
    if not request.user.is_staff:
        return redirect("menu-list")

    # --- KPI counts ---
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status="pending").count()
    total_customers = CustomerProfile.objects.count()
    total_menu_items = MenuItem.objects.filter(is_available=True).count()

    # --- Recent orders (last 10) ---
    recent_orders = (
        Order.objects.select_related("customer")
        .prefetch_related("items__menu_item")
        .order_by("-created_at")[:10]
    )

    # --- Line chart: orders per day for the last 7 days ---
    today = timezone.now().date()
    seven_days_ago = today - timedelta(days=6)

    # Fetch counts grouped by date
    from django.db.models import Count
    from django.db.models.functions import TruncDate

    daily_counts = (
        Order.objects.filter(created_at__date__gte=seven_days_ago)
        .annotate(day=TruncDate("created_at"))
        .values("day")
        .annotate(count=Count("id"))
    )

    # Build a dict keyed by date for fast lookup
    counts_by_date = {entry["day"]: entry["count"] for entry in daily_counts}

    # Produce a complete 7-day series, filling gaps with 0
    chart_labels = []
    chart_data = []
    for offset in range(7):
        day = seven_days_ago + timedelta(days=offset)
        chart_labels.append(day.strftime("%b %d"))
        chart_data.append(counts_by_date.get(day, 0))

    chart_labels_json = json.dumps(chart_labels, cls=DjangoJSONEncoder)
    chart_data_json = json.dumps(chart_data, cls=DjangoJSONEncoder)

    context = {
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "total_customers": total_customers,
        "total_menu_items": total_menu_items,
        "recent_orders": recent_orders,
        "chart_labels_json": chart_labels_json,
        "chart_data_json": chart_data_json,
    }
    return render(request, "dashboard.html", context)

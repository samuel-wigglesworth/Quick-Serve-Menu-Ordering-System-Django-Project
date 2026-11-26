from django.urls import path

from .views import reports_view, sales_report

urlpatterns = [
    path("sales/", sales_report, name="sales-report"),
    path("", reports_view, name="reports"),
]

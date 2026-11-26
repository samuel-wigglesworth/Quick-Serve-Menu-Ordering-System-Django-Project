from django.contrib import admin
from django.urls import include, path

from .views import dashboard

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("customers/", include("customers.urls")),
    path("menu/", include("menu.urls")),
    path("orders/", include("orders.urls")),
    path("delivery/", include("delivery.urls")),
    path("reports/", include("reports.urls")),
    path("", dashboard, name="dashboard"),
]

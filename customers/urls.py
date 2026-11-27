from django.urls import path

from .views import customer_delete, customer_edit, customer_list, profile_view

urlpatterns = [
    path("profile/", profile_view, name="customer-profile"),
    path("list/", customer_list, name="customer-list"),
    path("<int:pk>/edit/", customer_edit, name="customer-edit"),
    path("<int:pk>/delete/", customer_delete, name="customer-delete"),
]

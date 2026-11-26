from django.urls import path

from .views import (
    delivery_create,
    delivery_delete,
    delivery_list,
    delivery_track,
    delivery_update,
)

urlpatterns = [
    path("<int:order_id>/track/", delivery_track, name="delivery-track"),
    path("<int:order_id>/update/", delivery_update, name="delivery-update"),
    path("list/", delivery_list, name="delivery-list"),
    path("create/", delivery_create, name="delivery-create"),
    path("<int:status_id>/delete/", delivery_delete, name="delivery-delete"),
]

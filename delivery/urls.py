from django.urls import path

from .views import delivery_track, delivery_update

urlpatterns = [
    path("<int:order_id>/track/", delivery_track, name="delivery-track"),
    path("<int:order_id>/update/", delivery_update, name="delivery-update"),
]

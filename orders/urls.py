from django.urls import path

from .views import order_create, order_history, order_manage

urlpatterns = [
    path("create/", order_create, name="order-create"),
    path("history/", order_history, name="order-history"),
    path("<int:order_id>/manage/", order_manage, name="order-manage"),
]

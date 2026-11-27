from django.urls import path

from .views import order_cancel, order_create, order_delete, order_detail, order_history, order_manage

urlpatterns = [
    path("create/", order_create, name="order-create"),
    path("history/", order_history, name="order-history"),
    path("<int:pk>/detail/", order_detail, name="order-detail"),
    path("<int:order_id>/cancel/", order_cancel, name="order-cancel"),
    path("<int:order_id>/delete/", order_delete, name="order-delete"),
    path("<int:order_id>/manage/", order_manage, name="order-manage"),
]

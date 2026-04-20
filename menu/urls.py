from django.urls import path

from .views import menu_list, menu_manage

urlpatterns = [
    path("", menu_list, name="menu-list"),
    path("manage/", menu_manage, name="menu-manage"),
]

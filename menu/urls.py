from django.urls import path

from .views import menu_add, menu_delete, menu_edit, menu_list, menu_manage

urlpatterns = [
    path("", menu_list, name="menu-list"),
    path("manage/", menu_manage, name="menu-manage"),
    path("manage/add/", menu_add, name="menu-add"),
    path("manage/<int:pk>/edit/", menu_edit, name="menu-edit"),
    path("manage/<int:pk>/delete/", menu_delete, name="menu-delete"),
]

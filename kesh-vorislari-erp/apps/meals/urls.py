from django.urls import path

from . import views

app_name = "meals"

urlpatterns = [
    path("", views.menu_list, name="list"),
    path("menus/new/", views.menu_create, name="create"),
    path("menus/<int:pk>/", views.menu_detail, name="detail"),
    path("menus/<int:pk>/edit/", views.menu_update, name="update"),
    path("catalog/new/", views.meal_create, name="meal-create"),
]

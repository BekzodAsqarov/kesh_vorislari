from django.urls import path

from . import views

app_name = "groups"

urlpatterns = [
    path("", views.group_list, name="list"),
    path("new/", views.group_create, name="create"),
    path("<int:pk>/", views.group_detail, name="detail"),
    path("<int:pk>/edit/", views.group_update, name="update"),
]

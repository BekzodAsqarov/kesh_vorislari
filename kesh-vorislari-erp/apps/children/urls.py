from django.urls import path

from . import views

app_name = "children"

urlpatterns = [
    path("", views.child_list, name="list"),
    path("new/", views.child_create, name="create"),
    path("<int:pk>/", views.child_detail, name="detail"),
    path("<int:pk>/edit/", views.child_update, name="update"),
]

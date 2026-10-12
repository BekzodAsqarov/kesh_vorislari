from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("me/", views.profile_view, name="profile"),
    path("users/", views.user_list, name="users"),
    path("users/new/", views.user_create, name="user-create"),
    path("users/<int:pk>/edit/", views.user_update, name="user-update"),
]

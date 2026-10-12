from django.urls import path

from .web_views import index

app_name = "dashboard"

urlpatterns = [
    path("", index, name="index"),
]

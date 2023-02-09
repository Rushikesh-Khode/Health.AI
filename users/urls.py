from django.urls import path
from users.views import get_all

urlpatterns = [
    path("get/", get_all, name="getall"),
]


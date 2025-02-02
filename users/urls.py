from django.urls import path
from users.views import register_user, login_user, logout_user
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("register/", register_user, name="register_user"),
    path("login/", login_user, name="login_user"),
    path("logout/", logout_user, name="logout,users"),
]

urlpatterns = format_suffix_patterns(urlpatterns)

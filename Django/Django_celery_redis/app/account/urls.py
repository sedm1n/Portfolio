from django.urls import path
from .views import account_view, login_view, register_view, logout_view

app_name = "account"

urlpatterns = [
      path("", account_view, name="account_view"),
      path("login/", login_view, name="login_view"),
      path("register/", register_view, name="register_view"),
      path("logout/", logout_view, name="logout_view"),
]
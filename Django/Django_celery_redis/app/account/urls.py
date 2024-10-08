from django.shortcuts import render
from django.urls import path
from .views import register_view , user_login_view, user_logout_view

app_name = "account"

urlpatterns = [
      # path("", account_view, name="account_view"),
      # path("login/", login_view, name="login_view"),
      path("register/", register_view, name="register_view"),
      path("email-verification-sent/",
           lambda request: render(request, 
                                  "account/email/verification_sent.html") ,
                                    name="email_verification_sent"),
      
      path("login/", user_login_view, name="login_view"),
      path("logout/", user_logout_view, name="logout_view"),
]
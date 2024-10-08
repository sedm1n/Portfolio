from django.shortcuts import render
from django.urls import include, path
from .views import dashboard_view, delete_user_view, profile_manegment_view, register_view , user_login_view, user_logout_view

app_name = "account"

urlpatterns = [
      
      path("register/", register_view, name="register"),
      path("email-verification-sent/",
           lambda request: render(request, 
                                  "account/email/verification_sent.html") ,
                                    name="email_verification_sent"),
      path('password_reset/', include('django.contrib.auth.urls'), name="password_reset"),
      
      path("login/", user_login_view, name="login"),
      path("logout/", user_logout_view, name="logout"),

      path('dashboard/', dashboard_view, name="dashboard"),
      path('profile-managment/', profile_manegment_view, name="profile-management"),
      path('delete-user', delete_user_view, name="delete-user"),
]
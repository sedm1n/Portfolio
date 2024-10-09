from django.contrib.auth import views as auth_views
from django.shortcuts import render
from django.urls import include, path, reverse_lazy
from .views import dashboard_view, delete_user_view, profile_manegment_view, register_view , user_login_view, user_logout_view

app_name = "account"

urlpatterns = [
      
      path("register/", register_view, name="register"),
      path("email-verification-sent/",
           lambda request: render(request, 
                                  "account/email/verification_sent.html") ,
                                    name="email_verification_sent"),
      
      
      path("login/", user_login_view, name="login"),
      path("logout/", user_logout_view, name="logout"),

      path('dashboard/', dashboard_view, name="dashboard"),
      path('profile-managment/', profile_manegment_view, name="profile-management"),
      path('delete-user', delete_user_view, name="delete-user"),

      # password reset
      path('password-reset/',
           auth_views.PasswordResetView.as_view(
               success_url=reverse_lazy('account:password_reset_done'),
               template_name='account/password/password-reset.html',
               email_template_name='account/password/password-reset-email.html'
           ), name='password-reset'),

      path('password-reset/done/',
           auth_views.PasswordResetDoneView.as_view(
               template_name='account/password/password-reset-done.html'
           ), name='password-reset-done'),

      path('password-reset-confirm/<uidb64>/<token>/',
           auth_views.PasswordResetConfirmView.as_view(
               success_url=reverse_lazy('account:password_reset_complete'),
               template_name='account/password/password-reset-confirm.html'
           ), name='password-reset-confirm'),

      path('password-reset-complete/',
           auth_views.PasswordResetCompleteView.as_view(
               template_name='account/password/password-reset-complete.html'
           ), name='password-reset-complete'),
]
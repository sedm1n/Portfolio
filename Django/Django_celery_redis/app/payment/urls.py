from django.urls import path
from . import views

app_name = "payment"

urlpatterns = [

      path("chekout/", views.chekout_view, name="checkout"),
      path("complete-order/", views.complete_order_view, name="complete_order"),
      path("payment_success/", views.payment_success_view, name="payment_success"),
      path("payment_fail/", views.payment_fail_view, name="payment_fail"),
      path("shipping/", views.shipping_view, name="shipping"),

]
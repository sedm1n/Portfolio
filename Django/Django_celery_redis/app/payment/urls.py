from django.urls import path

from . import views
from .webhooks import stripe_webhook

app_name = "payment"

urlpatterns = [

      path("chekout/", views.chekout_view, name="checkout"),
      path("complete-order/", views.complete_order_view, name="complete-order"),
      path("payment_success/", views.payment_success_view, name="payment_success"),
      path("payment_fail/", views.payment_fail_view, name="payment_fail"),
      path("shipping/", views.shipping_view, name="shipping"),
      path("webhook-stripe/", stripe_webhook, name="webhook-stripe"),
      path("webhook-yookassa/", stripe_webhook, name="webhook-yookassa"),
      path("order/<int:order_id>/pdf/", views.admin_order_pdf, name="admin_order_pdf"),

]
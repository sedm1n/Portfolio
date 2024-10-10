from celery import shared_task

from django.conf import settings
from django.core.mail import send_mail

from .models import Order, ShippingAdress


@shared_task
def send_order_confirmation(order_id):
      order = Order.objects.get(id=order_id)
      
      subject = f'Заказ No {order.id}'
      recipient_data = ShippingAdress.objects.get(user=order.user)
      recipient_email = recipient_data.email
      message = f"Your order {order.id} has been confirmed. Thank you for shopping with us!"

      mail_to_sender = send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient_email])

      return mail_to_sender
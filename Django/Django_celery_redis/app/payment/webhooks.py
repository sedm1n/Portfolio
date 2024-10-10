import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from yookassa import Configuration, Payment, Webhook
from yookassa.domain.common import SecurityHelper
from yookassa.domain.notification import (
    WebhookNotificationEventType,
    WebhookNotificationFactory,
)

from .models import Order
from .tasks import send_order_confirmation


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        if session.mode == "payment" and session.payment_status == "paid":
            try:
                order_id = session.client_reference_id
            except Order.DoesNotExist:
                return HttpResponse(status=404)

        order = Order.objects.get(id=order_id)
        order.paid = True
        order.save()

    return HttpResponse(status=200)


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def yookassa_webhook(request):
    webhook = Webhook(request.body, request.headers["Content-Type"])
    event = webhook.parse()

   

    ip = get_client_ip(request)
    if not SecurityHelper().is_ip_trusted(ip):
        return HttpResponse(status=400)

    event_json = json.loads(request.body)
    try:
        notification_object = WebhookNotificationFactory().create(event_json)
        response_object = notification_object.object
        if notification_object.event == WebhookNotificationEventType.PAYMENT_SUCCEEDED:
            some_data = {
                "paymentId": response_object.id,
                "paymentStatus": response_object.status,
            }

        elif notification_object.event == WebhookNotificationEventType.PAYMENT_CANCELED:
            some_data = {
                "paymentId": response_object.id,
                "paymentStatus": response_object.status,
            }
        else:
            return HttpResponse(status=400)  # Сообщаем кассе об ошибке

        Configuration.configure("XXXXXX", "test_XXXXXXXX")

        payment_info = Payment.find_one(some_data["paymentId"])
        if payment_info:
            payment_status = payment_info.status

        else:
            return HttpResponse(status=400)

    except Exception:
        return HttpResponse(status=400)

    return HttpResponse(status=200)

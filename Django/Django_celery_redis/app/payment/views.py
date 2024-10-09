import uuid
from decimal import Decimal

import stripe
from cart.cart import Cart
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.conf import settings

from yookassa import Payment, Configuration as yoo_config

from .forms import ShippingAdressForm
from .models import Order, OrderItem, ShippingAdress


stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

yoo_config.account_id = settings.YOOKASSA_SHOP_ID
yoo_config.secret_key = settings.YOOKASSA_SECRET_KEY



def chekout_view(request):
    if request.user.is_authenticated:
        shipping_address = get_object_or_404(ShippingAdress, user=request.user)
        if shipping_address:
            return render(
                request, "payment/chekout.html", {"shipping_address": shipping_address}
            )
    return render(request, "payment/chekout.html")


def create_order(cart, user, shipping_address, total_price):
    """Создание заказа и элементов заказа."""
    if user.is_authenticated:
        order = Order.objects.create(user=user, shipping_address=shipping_address, amount=total_price)
    else:
        order = Order.objects.create(shipping_address=shipping_address, amount=total_price)

    for item in cart:
        OrderItem.objects.create(
            order=order,
            product=item['product'],
            price=item['price'],
            quantity=item['qty'],
            user=user if user.is_authenticated else None
        )
    
    return order

def prepare_stripe_session(cart, total_price, request, order_id):
    """Подготовка данных для Stripe-сессии."""
    session_data = {
        'mode': 'payment',
        'success_url': request.build_absolute_uri(reverse('payment:payment-success')),
        'cancel_url': request.build_absolute_uri(reverse('payment:payment-failed')),
        'line_items': []
    }

    for item in cart:
        session_data['line_items'].append({
            'price_data': {
                'unit_amount': int(item['price'] * Decimal(100)),
                'currency': 'usd',
                'product_data': {
                    'name': item['product']
                },
            },
            'quantity': item['qty'],
        })

    session_data['client_reference_id'] = order_id
    return stripe.checkout.Session.create(**session_data)

def prepare_yookassa_payment(total_price, request):
    """Подготовка данных для платежа через YooKassa."""
    idempotence_key = uuid.uuid4()

    payment = Payment.create({
        "amount": {
            "value": str(total_price * 93),  # Можно добавить логику для конвертации валюты
            "currency": 'RUB'
        },
        "confirmation": {
            "type": "redirect",
            "return_url": request.build_absolute_uri(reverse('payment:payment-success')),
        },
        "capture": True,
        "test": True,
        "description": 'Товары в корзине',
    }, idempotence_key)

    return payment.confirmation.confirmation_url

def complete_order_view(request):
    if request.method == 'POST':
        payment_type = request.POST.get('stripe-payment', 'yookassa-payment')

        # Получение данных формы
        name = request.POST.get('name')
        email = request.POST.get('email')
        street_address = request.POST.get('street_address')
        apartment_address = request.POST.get('apartment_address')
        country = request.POST.get('country')
        zip = request.POST.get('zip')
        cart = Cart(request)
        total_price = cart.get_total_price()

        # Получение или создание адреса доставки
        shipping_address, _ = ShippingAdress.objects.get_or_create(
            user=request.user,
            defaults={
                'name': name,
                'email': email,
                'street_address': street_address,
                'apartment_address': apartment_address,
                'country': country,
                'zip': zip
            }
        )

        # Обработка различных методов оплаты
        if payment_type == "stripe-payment":
            order = create_order(cart, request.user, shipping_address, total_price)
            session = prepare_stripe_session(cart, total_price, request, order.id)
            return redirect(session.url, code=303)

        elif payment_type == "yookassa-payment":
            order = create_order(cart, request.user, shipping_address, total_price)
            confirmation_url = prepare_yookassa_payment(total_price, request)
            return redirect(confirmation_url)


def payment_success_view(request):
    for key in list(request.session.keys()):
        del request.session[key]

    return render(request, "payment/payment-success.html")


def payment_fail_view(request):
    return render(request, "payment/payment-failed.html")


@login_required(login_url="account:login")
def shipping_view(request):
    try:
        shipping_adress = ShippingAdress.objects.get(user=request.user)
    except ShippingAdress.DoesNotExist:
        shipping_adress = None

    form = ShippingAdressForm(instance=shipping_adress)

    if request.method == "POST":
        form = ShippingAdressForm(request.POST, instance=shipping_adress)
        if form.is_valid():
            shipping_adress = form.save(commit=False)
            shipping_adress.user = request.user
            shipping_adress.save()
            return redirect("account:dashboard")

    return render(request, "payment/shipping/shipping.html", {"form": form})

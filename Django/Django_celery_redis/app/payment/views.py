from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from cart.cart import Cart
from .forms import ShippingAdressForm
from .models import ShippingAdress, Order, OrderItem


def chekout_view(request):
    if request.user.is_authenticated:
        shipping_address = get_object_or_404(ShippingAdress, user=request.user)
        if shipping_address:
            return render(
                request, "payment/chekout.html", {"shipping_address": shipping_address}
            )
    return render(request, "payment/chekout.html")


def complete_order_view(request):
    
    if request.POST.get("action") == "payment":
        name = request.POST.get("name")
        email = request.POST.get("email")
        street_address = request.POST.get("address1")
        apartment_address = request.POST.get("address2")
        country = request.POST.get("country")
        zipcode = request.POST.get("zipcode")

        cart = Cart(request)
        total_price = cart.get_total_price()
        shipping_address, _ = ShippingAdress.objects.get_or_create(
            user=request.user,
            defaults={
                "full_name": name,
                "email": email,
                "street_adress": street_address,
                "apartment_adress": apartment_address,
                "country": country,
                "zip": zipcode,
            },
        )
        
        if request.user.is_authenticated:
            order = Order.objects.create(
                user=request.user, shipping_address=shipping_address, amount=total_price
            )
        
            for item in cart:
                  OrderItem.objects.create(
                  order=order,
                  product=item["product"],
                  price=item["price"],
                  quantity=item["qty"],
                  user = request.user
                  )
        else:
            order = Order.objects.create(
                shipping_address=shipping_address, amount=total_price
            )
            for item in cart:
                  OrderItem.objects.create(
                  order=order,
                  product=item["product"],
                  price=item["price"],
                  quantity=item["qty"],
                  
                  )


        
        return JsonResponse({"success": True})
    else:
        print("get")
        return JsonResponse({"success": False})  
#     return render(request, "payment/complete_order.html")


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

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from cart.cart import Cart
from .forms import ShippingAdressForm
from .models import ShippingAdress, Order, OrderItem

def chekout_view(request):
      return render(request, 'payment/chekout.html')

def complete_order_view(request):
      return render(request, 'payment/complete_order.html')

def payment_success_view(request):
      return render(request, 'payment/payment_success.html')

def payment_fail_view(request):
      return render(request, 'payment/payment_failed.html')

@login_required(login_url='account:login')
def shipping_view(request):
      try:
            shipping_adress = ShippingAdress.objects.get(user=request.user)
      except ShippingAdress.DoesNotExist:
            shipping_adress = None
      
      form = ShippingAdressForm(instance=shipping_adress))

      if request.method == 'POST':
            form = ShippingAdressForm(request.POST, instance=shipping_adress)
            if form.is_valid():
                  shipping_adress = form.save(commit=False)
                  shipping_adress.user = request.user
                  shipping_adress.save()
                  return redirect('account:dashboard')

      return render(request, 'payment/shipping/shipping.html', {'form': form})


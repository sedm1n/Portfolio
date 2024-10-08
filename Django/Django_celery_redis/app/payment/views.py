from django.shortcuts import render

def chekout_view(request):
      return render(request, 'payment/chekout.html')

def complete_order_view(request):
      return render(request, 'payment/complete_order.html')

def payment_success_view(request):
      return render(request, 'payment/payment_success.html')

def payment_fail_view(request):
      return render(request, 'payment/payment_failed.html')

def shipping_view(request):
      return render(request, 'payment/shipping/shipping.html')

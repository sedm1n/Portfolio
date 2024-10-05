from django.shortcuts import render, get_object_or_404
from shop.models import ProductProxy

from django.http import JsonResponse

def cart_view(request):
      render(request, 'cart/cart_view.html')
      
      
def cart_add(request):
      pass
def cart_delete(request):
      pass
def cart_update(request):
      pass


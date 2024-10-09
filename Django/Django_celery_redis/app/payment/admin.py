from django.contrib import admin
from .models import ShippingAdress, Order, OrderItem


admin.site.register(ShippingAdress) 
admin.site.register(Order) 
admin.site.register(OrderItem) 

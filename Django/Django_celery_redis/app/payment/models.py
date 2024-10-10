from django.db import models

from django.contrib.auth import get_user_model
from django.db import models

from shop.models import Product

User = get_user_model()


class ShippingAdress(models.Model):
    full_name = models.CharField(max_length=250)
    email = models.EmailField("email adress", max_length=254)
    street_adress = models.CharField(max_length=100)
    apartment_adress = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=12, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "ShippingAdress object: " + str(self.id)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    shipping_address = models.ForeignKey(
        ShippingAdress, on_delete=models.SET_NULL, null=True
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return "Order object: " + str(self.id)


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return "OrderItem object: " + str(self.id)

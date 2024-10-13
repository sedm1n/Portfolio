from decimal import Decimal
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

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

    class Meta:
        verbose_name = "Shipping Adress"
        verbose_name_plural = "Shipping Adresses"
        ordering = ['-id']

    def __str__(self):
        return "ShippingAdress object: " + " - " + self.full_name
    
    def get_absolute_url(self):
        return f"{reverse('payment:shipping')}"
    
    @classmethod
    def create_default_shipping_address(cls, user):
        default_shipping_address = {'user': user,
                                    'full_name': "Noname",
                                    'email': "example@example.com",
                                    'street_adress': "street",
                                    'apartment_adress': "apartment",
                                    'city': "city",
                                    'country': "country",
                                    'zip': "12345"}
        shipping_address = cls(**default_shipping_address)
        shipping_address.save()
        return shipping_address
    


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    shipping_address = models.ForeignKey(
        ShippingAdress, on_delete=models.SET_NULL, null=True
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0),MaxValueValidator(100)])

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ['-created']
        indexes=[models.Index(fields=['-created'])]

        constraints= [
            models.CheckConstraint(check=models.Q(amount__gte=0), name="amount_gte_0"),   
        ]

    def __str__(self):
        return "Order object: " + str(self.id)
    
    def get_absolute_url(self):
        return reverse("payment:order_detail", kwargs={"pk": self.pk})

    def get_total_cost_before_discount(self):
        return sum(item.get_cost() for item in self.items.all())
    
    @property
    def get_discount(self):
        if (total_cost := self.get_total_cost_before_discount()) and self.discount:
            return total_cost * (self.discount / Decimal(100))
        return Decimal(0)
    


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,related_name='items')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)


    class Meta:
        verbose_name = "OrderItem"
        verbose_name_plural = "OrderItems"
        ordering = ['-id']

        constraints= [
            models.CheckConstraint(check=models.Q(quantity__gte=0), name="quantity_gte_0"),   
        ]

    def __str__(self):
        return "OrderItem object: " + str(self.id)

    def get_cost(self):
        return self.price * self.quantity

    @classmethod
    def get_total_quantity_for_product(cls, product):
        return cls.objects.filter(product=product).aggregate(
            total_quantity=models.Sum('quantity'))['total_quantity'] or 0
    
    @staticmethod
    def average_price():
        return OrderItem.objects.aggregate(models.Avg('price'))['average_price']
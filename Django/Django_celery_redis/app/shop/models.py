from decimal import Decimal
import random
import string
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify
from django.urls import reverse




class Category(models.Model):
    """
    Category model

    Contains information about category
    """

    name = models.CharField(verbose_name="Название", max_length=150, db_index=True)
    parent = models.ForeignKey(
        "self",
        related_name="children",
        null=True,
        blank=True,
        verbose_name="Родитель",
        on_delete=models.CASCADE,
    )
    slug = models.SlugField(
        max_length=150,
        verbose_name="URL",
        unique=True,
        null=False,
    )
    created_at = models.DateTimeField(verbose_name="Создан", auto_now_add=True)

    class Meta:
        unique_together = ["slug", "parent"]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return " -> ".join(full_path[::-1])

    def _rand_slug():
        """
            Generates a random slug for a model instance.

            Returns a unique slug 3 characters long.
        """
        return "".join(
        random.choice(string.ascii_lowercase + string.digits) for _ in range(3)
            )


    def save(self, *args, **kwargs):
        """
        Save the category instance.

        If the `slug` is not set, generate a unique slug using the `slugify` function
        and the `rand_slug` function. The slug is then saved to the database.
        """
        if not self.slug:
            self.slug = slugify(self._rand_slug() + "-pickBetter" + self.name)
        super().save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse("shop:category_list", kwargs={"slug": self.slug})


class Product(models.Model):
    """
    Product model

    Contains information about product
    """

    title = models.CharField(verbose_name="Название", max_length=150, db_index=True)
    brand = models.CharField(verbose_name="Бренд", max_length=150)
    description = models.TextField(verbose_name="Описание")

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    slug = models.SlugField(
        max_length=150,
        verbose_name="URL",
        unique=True,
        null=False,
    )
    price = models.DecimalField(
        verbose_name="Цена", max_digits=10, decimal_places=2, default=0.00
    )

    image = models.ImageField("Изображение", upload_to="products/%Y/%m/%d", blank=True)
    available = models.BooleanField("Доступен", default=True)

    created_at = models.DateTimeField(verbose_name="Создан", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Обновлен", auto_now=True)
    discount  = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse("shop:product_detail", kwargs={"slug": self.slug})
    
    def get_discounted_price(self):
        discounted_price = self.price - (self.price * self.discount / Decimal(100))
        return round(discounted_price, 2)
    
    @property
    def full_image_url(self):
        return self.image.url if self.image else ""


class ProductManager(models.Manager):
    """
    Manager for the Product model, which provides a custom `get_queryset`
    method that filters out unavailable products.
    """

    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(available=True)


class ProductProxy(Product):
    objects = ProductManager()

    class Meta:
        proxy = True

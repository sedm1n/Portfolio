import random
import string
from django.db import models
from django.utils.text import slugify
from django.urls import reverse

def rand_slug():
    return "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(3))

# Create your models here.
class Category(models.Model):
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
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(rand_slug() + "-pickBetter" + self.name)
        super().save(*args, **kwargs)

#     def get_absolute_url(self):
#         return reverse("shop:category", kwargs={"slug": self.slug})

class Product(models.Model):
    title = models.CharField(verbose_name="Название", max_length=150, db_index=True)
    brang = models.CharField(verbose_name="Бренд", max_length=150)
    description = models.TextField(verbose_name="Описание")

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    slug = models.SlugField(
        max_length=150,
        verbose_name="URL",
        unique=True,
        null=False,
    )
    price = models.DecimalField(verbose_name="Цена", max_digits=10, decimal_places=2, default=0.00)

    image = models.ImageField("Изображение", upload_to="products/%Y/%m/%d", blank=True)
    available = models.BooleanField("Доступен", default=True)

    created_at = models.DateTimeField(verbose_name="Создан", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Обновлен", auto_now=True)  

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.title

#     def get_absolute_url(self):
#         return reverse("shop:product", kwargs={"slug": self.slug})
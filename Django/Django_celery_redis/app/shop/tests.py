from ast import List
from django.template.defaultfilters import first
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from .models import Category, ProductProxy, Product


class ProductViewTest(TestCase):
    def test_get_products(self):
        small_gif = (
            b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04"
            b"\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02"
            b"\x02\x4c\x01\x00\x3b"
        )
        uploaded = SimpleUploadedFile("small.gif", small_gif, content_type="image/gif")
        category = Category.objects.create(name="django")
        product_1 = Product.objects.create(
            title="product1",
            brand="django",
            description="django",
            category=category,
            slug="product1",
            price=100,
            image=uploaded,
            available=True,
        )
        product_2 = Product.objects.create(
            title="product2",
            brand="django2",
            description="django",
            category=category,
            slug="product2",
            price=100,
            image=uploaded,
            available=True,
        )

        response = self.client.get(reverse("shop:products"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["products"].count(), 2)
        self.assertEqual(list(response.context["products"]), [product_1, product_2])
        self.assertContains(response, product_1)


class ProductDetailViewTest(TestCase):
    def test_get_product_by_slug(self):
        small_gif = (
            b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04"
            b"\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02"
            b"\x02\x4c\x01\x00\x3b"
        )
        uploaded = SimpleUploadedFile("small.gif", small_gif, content_type="image/gif")
        category = Category.objects.create(name="django")
        product = Product.objects.create(
            title="product1",
            brand="django",
            description="django",
            category=category,
            slug="product1",
            price=100,
            image=uploaded,
            available=True,
        )

        response = self.client.get(
            reverse("shop:product_detail", kwargs={"slug": product.slug})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["product"], product)
        self.assertEqual(response.context["product"].slug, product.slug)
        self.assertContains(response, product)


class CategoryListViewTest(TestCase):
    def setUp(self) -> None:
        small_gif = (
            b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04"
            b"\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02"
            b"\x02\x4c\x01\x00\x3b"
        )
        uploaded = SimpleUploadedFile("small.gif", small_gif, content_type="image/gif")
        self.category = Category.objects.create(name="django", slug="django")
        self.product = ProductProxy.objects.create(
            title="Test product",
            brand="django",
            description="django",
            category=self.category,
            slug="test-product",
            price=100,
            image=uploaded,
            available=True,
        )
    def  test_status_code(self):
        response = self.client.get(
            reverse("shop:category_list", 
                    kwargs={"slug": self.category.slug}))
        self.assertEqual(response.status_code, 200)
    def test_template_used(self):
        response = self.client.get(reverse("shop:category_list", 
                                           args=[self.category.slug]))  
        self.assertTemplateUsed(response,"shop/category_list.html")

    def test_context_data(self):
        response = self.client.get(reverse("shop:category_list",
                                           args=[self.category.slug]))
        self.assertEqual(response.context["category"], self.category)
        self.assertEqual(response.context["products"].first(), self.product)

import json

from django.test import TestCase

from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory, Client
from django.urls import reverse

from shop.models import ProductProxy, Category

from .views import cart_view, cart_add, cart_delete, cart_update

class CartViewTest(TestCase):
      def setUp(self) -> None:
            self.client = Client()
            self.factory = RequestFactory().get(
                reverse("cart:cart_view"))
            self.middleware = SessionMiddleware(self.factory)
            self.middleware.process_request(self.factory)
            self.factory.session.save()

      def test_cart_view(self):
            request = self.factory
            response = cart_view(request)

            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(self.client.get(
                reverse("cart:cart_view")), "cart/cart_view.html")

class CartAddTest(TestCase):
      def setUp(self) -> None:
            
            self.category = Category.objects.create(
                name="category1_test", slug="category1_test")
            
            
            self.product = ProductProxy.objects.create(
                title="Test product",price = 10, category = self.category
            )

            self.factory = RequestFactory().post(
                reverse("cart:add_to_cart"), {
                      'action': 'post',
                      'product_id': self.product.id,
                      'product_qty': 2
                })
            self.middleware = SessionMiddleware(self.factory)
            self.middleware.process_request(self.factory)
            self.factory.session.save()

      def test_cart_add(self):
            request = self.factory
            response = cart_add(request)

            self.assertEqual(response.status_code, 200)

            data = json.loads(response.content)
            self.assertEqual(data['product'], 'Test product')
            self.assertEqual(data['qty'], 2)


class CartDeleteTest(TestCase):
      def setUp(self) -> None:
            self.category = Category.objects.create(
                name="category1_test", slug="category1_test")
            
            
            self.product = ProductProxy.objects.create(
                title="Test product",price = 10, category = self.category
            )
            self.factory = RequestFactory().post(
                reverse("cart:delete-to-cart"), {
                    'action': 'post',
                    'product_id': self.product.id
                })
            self.middleware = SessionMiddleware(self.factory)
            self.middleware.process_request(self.factory)
            self.factory.session.save()

      def test_cart_delete(self):
            request = self.factory
            response = cart_delete(request)

            self.assertEqual(response.status_code, 200)

            data = json.loads(response.content)
            self.assertEqual(data['qty'], 0)
            self.assertEqual(data['total'], 0)


class CartUpdateTest(TestCase):
      def setUp(self) -> None:
            self.category = Category.objects.create(
                name="category1_test", slug="category1_test")
            
            
            self.product = ProductProxy.objects.create(
                title="Test product",price = 10, category = self.category
            )
            self.factory = RequestFactory().post(
                reverse("cart:add_to_cart"), {
                      'action': 'post',
                      'product_id': self.product.id,
                      'product_qty': 2
                })
            self.factory = RequestFactory().post(
                reverse("cart:update-to-cart"), {
                    'action': 'post',
                    'product_id': self.product.id,
                    'product_qty': 5
                })
            
            self.middleware = SessionMiddleware(self.factory)
            self.middleware.process_request(self.factory)
            self.factory.session.save()

      def test_cart_update(self):
            request = self.factory
            response = cart_add(request)
            response = cart_update(request)

            self.assertEqual(response.status_code, 200)
            data = json.loads(response.content)

            self.assertEqual(data['total'], '50.00')
            self.assertEqual(data['qty'], 5)
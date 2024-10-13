from django.core.management import BaseCommand
from faker import Faker
from stripe import Discount

from shop.models import Category, Product

fake = Faker()


class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker()

        for _ in range(20):
            product_title = fake.name()
            product_brand = fake.company()
            product_description = fake.paragraph(nb_sentences=2)
            product_price = fake.random_int(min=1, max=1000)

            category = Category.objects.first()
            product = Product(
                category=category,
                title=product_title,
                brand=product_brand,
                description=product_description,
                price=product_price,
                slug = fake.slug(),
                available=True,
                created_at = fake.date_time_this_year(),
                updated_at = fake.date_time_this_year(),
                discount = fake.random_int(min=0, max=30),
            )

            product.save()

        self.stdout.write(self.style.SUCCESS("Successfully created products"))

# Generated by Django 5.1.1 on 2024-10-13 08:21

import django.core.validators
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_order_paid'),
        ('shop', '0002_rename_brang_product_brand'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-created'], 'verbose_name': 'Order', 'verbose_name_plural': 'Orders'},
        ),
        migrations.AlterModelOptions(
            name='orderitem',
            options={'ordering': ['-id'], 'verbose_name': 'OrderItem', 'verbose_name_plural': 'OrderItems'},
        ),
        migrations.AlterModelOptions(
            name='shippingadress',
            options={'ordering': ['-id'], 'verbose_name': 'Shipping Adress', 'verbose_name_plural': 'Shipping Adresses'},
        ),
        migrations.AddField(
            model_name='order',
            name='discount',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['-created'], name='payment_ord_created_6a6f0c_idx'),
        ),
        migrations.AddConstraint(
            model_name='order',
            constraint=models.CheckConstraint(condition=models.Q(('amount__gte', 0)), name='amount_gte_0'),
        ),
        migrations.AddConstraint(
            model_name='orderitem',
            constraint=models.CheckConstraint(condition=models.Q(('quantity__gte', 0)), name='quantity_gte_0'),
        ),
    ]

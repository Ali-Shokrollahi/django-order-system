# Generated by Django 5.1.6 on 2025-03-15 06:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['price'], name='idx_product_price'),
        ),
    ]

# Generated by Django 4.1.3 on 2023-03-07 07:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceapp', '0004_orders_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='credit',
            field=models.DecimalField(decimal_places=2, default=django.utils.timezone.now, max_digits=6),
            preserve_default=False,
        ),
    ]

# Generated by Django 4.2.17 on 2025-01-25 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netsapp', '0006_alter_billingaddress_user_alter_order_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='total_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]

# Generated by Django 4.1.7 on 2024-10-29 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0030_receiptproduct_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='receiptproduct',
            name='product_name',
            field=models.CharField(blank=True, max_length=264, verbose_name='Продукт'),
        ),
    ]

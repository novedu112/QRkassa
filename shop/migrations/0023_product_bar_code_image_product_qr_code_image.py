# Generated by Django 4.1.7 on 2024-10-12 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0022_remove_receipt_product_receiptproduct_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='bar_code_image',
            field=models.ImageField(blank=True, upload_to='products/qr_code_image/', verbose_name='Фото QR кода'),
        ),
        migrations.AddField(
            model_name='product',
            name='qr_code_image',
            field=models.ImageField(blank=True, upload_to='products/barcode_image/', verbose_name='Фото штрих кода'),
        ),
    ]

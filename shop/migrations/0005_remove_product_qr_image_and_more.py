# Generated by Django 4.1.7 on 2024-09-19 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_product_discount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='qr_image',
        ),
        migrations.AddField(
            model_name='product',
            name='manufacturer_barcode_image',
            field=models.ImageField(blank=True, upload_to='products/manufacturer_barcode_image/', verbose_name='Фото QR кода производителя'),
        ),
        migrations.AddField(
            model_name='product',
            name='manufacturer_qr_code_image',
            field=models.ImageField(blank=True, upload_to='products/manufacturer_qr_code_image/', verbose_name='Фото QR кода производителя'),
        ),
        migrations.AddField(
            model_name='product',
            name='my_generated_bar_code_image',
            field=models.ImageField(blank=True, upload_to='products/my_generated_bar_code_image/', verbose_name='Фото штрих кода сгенерированного нами'),
        ),
        migrations.AddField(
            model_name='product',
            name='my_generated_qr_code_image',
            field=models.ImageField(blank=True, upload_to='products/my_generated_qr_code_image/', verbose_name='Фото QR кода сгенерированного нами'),
        ),
    ]

# Generated by Django 4.1.7 on 2024-09-19 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_remove_product_qr_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, upload_to='products/images/', verbose_name='Фото'),
        ),
    ]

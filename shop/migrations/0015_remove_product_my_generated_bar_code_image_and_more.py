# Generated by Django 4.1.7 on 2024-09-21 05:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_product_manufacturer_barcode_text_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='my_generated_bar_code_image',
        ),
        migrations.RemoveField(
            model_name='product',
            name='my_generated_bar_code_text',
        ),
    ]

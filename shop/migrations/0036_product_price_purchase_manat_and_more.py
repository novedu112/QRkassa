# Generated by Django 4.1.7 on 2024-11-10 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0035_product_kurs_alter_product_price_purchase_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price_purchase_manat',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Цена покупки manat'),
        ),
        migrations.AddField(
            model_name='product',
            name='price_sale_manat',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Цена продажи manat'),
        ),
        migrations.AddField(
            model_name='product',
            name='price_sale_optom_manat',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Цена Оптовой продажи manat'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price_purchase',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена покупки'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price_sale',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена продажи'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price_sale_optom',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Цена Оптовой продажи'),
        ),
    ]

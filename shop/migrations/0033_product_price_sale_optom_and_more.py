# Generated by Django 4.1.7 on 2024-11-04 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0032_receiptproduct_product_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price_sale_optom',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Цена Оптовой продажи'),
        ),
        migrations.AlterField(
            model_name='actionhistory',
            name='action_type',
            field=models.CharField(choices=[('CHANGE_PRODUCT', 'Добавление-Изменение продукта'), ('CHANGE_RECEIPT', 'Отмена квитанции'), ('CHANGE_DISCOUNT', 'Изменение скидки по категориям'), ('SET_SELL_PRICE', 'Установить цену по категориям')], max_length=50, verbose_name='Тип действия'),
        ),
    ]

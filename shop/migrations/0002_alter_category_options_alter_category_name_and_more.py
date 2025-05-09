# Generated by Django 4.1.7 on 2024-09-10 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категорию', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='shop.category', verbose_name='Категория продукта'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(verbose_name='Описание продукта'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to='products/images/', verbose_name='Фото'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Название продукта'),
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
            name='profit',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, verbose_name='Прибыль'),
        ),
        migrations.AlterField(
            model_name='product',
            name='stock',
            field=models.PositiveIntegerField(default=0, verbose_name='Количество на складе'),
        ),
    ]

# Generated by Django 4.1.7 on 2024-11-10 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0040_receipt_total_manat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receipt',
            name='total_manat',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Сумма квитанции манат'),
        ),
    ]

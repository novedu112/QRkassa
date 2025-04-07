from django.db import models
from django.contrib.auth.models import User

import qrcode
from barcode import Code128
from io import BytesIO
from django.core.files.base import ContentFile
from django.db import models
import barcode
from barcode.writer import ImageWriter
from django.utils.text import slugify
from django.db.models import F
from django.core.exceptions import ValidationError

from decimal import Decimal
# для custom_slugify
import re
from unidecode import unidecode


def custom_slugify(value):
    """
    Преобразует строку в slug.
    Применяет транслитерацию для русских символов и удаляет нежелательные символы.
    """
    # Применяем транслитерацию для русских букв
    value = unidecode(value)  # Преобразование русских букв в латиницу
    value = value.lower()  # Приводим все к нижнему регистру
    value = re.sub(r'[^a-z0-9-]', '-', value)  # Заменяем все недопустимые символы на дефисы
    value = re.sub(r'-+', '-', value)  # Заменяем несколько дефисов на один
    value = value.strip('-')  # Удаляем ведущие и завершающие дефисы
    return value



class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Категория')
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        # if not self.slug or self.slug != slugify(self.name):
        self.slug = custom_slugify(self.name)
        super().save(*args, **kwargs)

        



    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'


class Kurs(models.Model):
    kurs = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Курс', default=0)

    def __str__(self):
        return str(self.kurs)

    def save(self, *args, **kwargs):
        # Проверяем, существует ли уже запись
        if Kurs.objects.exists() and not self.pk:
            raise ValidationError('Можно создать только одну запись для курса.')

        # Проверка, чтобы курс не был отрицательным
        if float(self.kurs) < 0:
            raise ValidationError('Курс не может быть отрицательным.')

        super().save(*args, **kwargs)

        # Пересчет цен всех продуктов
        Product.objects.all().update(
            price_purchase_manat=F('price_purchase') * self.kurs,
            price_sale_manat=F('price_sale') * self.kurs,
            price_sale_optom_manat=F('price_sale_optom') * self.kurs,
        )



class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название продукта')
    slug = models.SlugField(max_length=250, verbose_name='slug', unique=True, blank=True)
    # description = models.TextField(verbose_name='Описание продукта', blank=True)
    price_purchase = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена покупки')
    price_sale = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена продажи')
    price_sale_optom = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена Оптовой продажи', default=0)
    cubic_meter = models.DecimalField(max_digits=10, decimal_places=3, verbose_name='Кубический метр', default=0)

    price_purchase_manat = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена покупки manat', default=0)
    price_sale_manat = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена продажи manat', default=0 )
    price_sale_optom_manat = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена Оптовой продажи manat', default=0)

    # kurs = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='kurs', default=0)
    

    # price_sale_with_discount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена продажи со скидкой', blank=True, default=True)  # # не успользуем

    # profit = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Прибыль', blank=True, default=0)  # не успользуем
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория продукта')
    # image = models.ImageField(upload_to='products/images/', verbose_name='Фото', blank=True)

    code_image = models.ImageField(upload_to='products/code_image/', verbose_name='Фото QR кода', blank=True)
    code_text = models.CharField(max_length=300, verbose_name='Текст QR кода', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    stock = models.DecimalField(max_digits=10, decimal_places=3, default=0, verbose_name='Количество на складе (по весу в кг, или по штучно)')
    # discount = models.PositiveIntegerField(default=0, verbose_name='Скидка на продукт (%)') # не успользуем

    def clean(self):
        # Валидация: цена продажи не должна быть меньше цены закупки
        if self.price_sale < self.price_purchase:
            raise ValidationError('Цена продажи не может быть меньше цены закупки.')


    def save(self, *args, **kwargs):
        # if self.discount:
        #     price_sale = Decimal(self.price_sale)
        #     price_purchase = Decimal(self.price_purchase)
        #     discount = Decimal(self.discount)

        #     self.profit = price_sale - (price_sale * (discount/100)) - price_purchase # - (price_sale * (discount/100))
        # else:
        #     print('gggg', self.price_sale)
        #     print('gggg2', self.price_purchase)
        #     self.profit = Decimal(self.price_sale) - Decimal(self.price_purchase)  

        # конверт доллара в манаты
        kurs_record = Kurs.objects.first()
        if kurs_record and kurs_record.kurs > 0:
            kurs = kurs_record.kurs
            self.price_purchase_manat = Decimal(self.price_purchase) * Decimal(kurs)
            self.price_sale_manat = Decimal(self.price_sale) * Decimal(kurs)
            self.price_sale_optom_manat = Decimal(self.price_sale_optom) * Decimal(kurs)


        if not self.slug: 
            self.slug = custom_slugify(self.name)

        # if self.discount > 0:
        #     self.price_sale_with_discount = Decimal(self.price_sale) - Decimal((Decimal(self.price_sale) * Decimal((Decimal(self.discount)/100))))
        # else:
        #     self.price_sale_with_discount = self.price_sale
        super().save(*args, **kwargs)


        # if not self.manufacturer_qr_code_image:
            # manufacturer_qr = qrcode.make(self.id)
            # self.manufacturer_qr_code_text = self.id
            # # Сохранение QR-кода в байтовый поток
            # buffer = BytesIO()
            # manufacturer_qr.save(buffer, format='PNG')
            # file_name = f'manufacturer_qr_code_{self.id}.png'
            # self.manufacturer_qr_code_image.save(file_name, ContentFile(buffer.getvalue()), save=False)
        
        # если нет qr кода производителя то надо сгенерировать свое, а qr производителя пусть будет пустой
        # if not self.manufacturer_qr_code_image:
            # my_generated_qr = qrcode.make(f"an{str(self.id)}")
            # self.my_generated_qr_code_text = f"an{self.id}"
            # # Сохранение QR-кода в байтовый поток
            # buffer = BytesIO()
            # my_generated_qr.save(buffer, format='PNG')
            # file_name = f'an{self.id}.png'
            # self.my_generated_qr_code_image.save(file_name, ContentFile(buffer.getvalue()), save=False)
        
        if self.code_text:
            QR = qrcode.make(self.code_text)
            buffer = BytesIO()
            QR.save(buffer, format='PNG')
            QR_name = f"{self.code_text}.png"
            self.code_image.save(QR_name, ContentFile(buffer.getvalue()), save=False)

        # if self.bar_code_text:
            # # bar = barcode.get('ean13', str(self.bar_code_text).zfill(12), writer=ImageWriter())
            # # buffer = BytesIO()
            # # bar.write(buffer)
            # # bar_name = f'{self.bar_code_text}.png'
            # # self.bar_code_image.save(bar_name, ContentFile(buffer.getvalue()), save=False)
            #  # Убираем пробелы

            # cleaned_barcode = str(self.bar_code_text).strip()

            # # Генерируем штрих-код Code 128
            # bar = Code128(cleaned_barcode, writer=ImageWriter())
            # buffer = BytesIO()
            
            # # Запись штрих-кода в буфер
            # bar.write(buffer)
            
            # # Название файла для сохранения
            # bar_name = f'{cleaned_barcode}.png'

            # # Сохранить изображение
            # self.bar_code_image.save(bar_name, ContentFile(buffer.getvalue()), save=False)
        
        # Если нет кода от производителя то создаем свой код и его текст
        if not self.code_text:
            self.code_text = f"ves{self.id}"
            QR = qrcode.make(self.code_text)
            buffer = BytesIO()
            QR.save(buffer, format='PNG')
            QR_name = f"{self.code_text}.png"
            self.code_image.save(QR_name, ContentFile(buffer.getvalue()), save=False)
        super().save(*args, **kwargs)
            


        # if not self.manufacturer_barcode_image:
        #     manufacturer_barcode = barcode.get('ean13', str(self.id).zfill(12), writer=ImageWriter())
        #     self.manufacturer_barcode_text = manufacturer_barcode
        #     buffer = BytesIO()
        #     manufacturer_barcode.write(buffer)
        #     file_name = f'manufacturer_barcode_{self.id}.png'
        #     self.manufacturer_barcode_image.save(file_name, ContentFile(buffer.getvalue()), save=False)

        # # если нет штрих кода производителя то надо сгенерировать свое, а штрих производителя пусть будет пустой
        # if not self.manufacturer_barcode_image:
        #     my_generated_bar_code = barcode.get('ean13', str(self.id).zfill(12), writer=ImageWriter())
        #     self.my_generated_bar_code_text = my_generated_bar_code
        #     buffer = BytesIO()
        #     my_generated_bar_code.write(buffer)
        #     file_name = f'my_generated_bar_code{self.id}.png'
        #     self.my_generated_bar_code_image.save(file_name, ContentFile(buffer.getvalue()), save=False)
            
        # super().save(*args, **kwargs)


    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at'])
        ]
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name

    

class ReceiptProduct(models.Model):
    receipt = models.ForeignKey('Receipt', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Количество')

    price_purchase = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена покупки', null=True, blank=True)
    price_sale = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена продажи', null=True, blank=True)
    profit = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Прибыль', null=True, blank=True, default=0)

    price_purchase_manat = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена покупки манат', null=True, blank=True)
    price_sale_manat = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена продажи манат', null=True, blank=True)
    profit_manat = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Прибыль манат', null=True, blank=True, default=0)

    # price_sale_with_discount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена продажи со скидкой', null=True, blank=True)  # не используем
    # discount = models.PositiveIntegerField(default=0, verbose_name='Скидка на продукт (%)') # не используем

    product_name = models.CharField(max_length=264, verbose_name="Продукт", blank=True)
    product_slug = models.CharField(max_length=264, verbose_name="Продукт slug", blank=True)

    class Meta:
        verbose_name = 'Продукт в квитанции'
        verbose_name_plural = 'Продукты в квитанции'

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


class Receipt(models.Model):
    kassir = models.ForeignKey(User, verbose_name='Кассир', on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, through='ReceiptProduct', verbose_name='Продукты')
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма квитанции')
    total_manat = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма квитанции манат', default=0)
    changed = models.BooleanField (default='False', verbose_name='Отменено')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата покупки')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата изменения квитанции')

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]
        verbose_name = 'Квитанция'
        verbose_name_plural = 'Квитанции'

    def __str__(self):
        return self.kassir.username




class ActionHistory(models.Model):
    ACTION_TYPES = [
        ('CHANGE_PRODUCT', 'Добавление-Изменение продукта'),
        ('CHANGE_RECEIPT', 'Отмена квитанции'),
        ('CHANGE_DISCOUNT', 'Изменение скидки по категориям'),
        ('SET_SELL_PRICE', 'Установить цену по категориям'),
        ('SET_KURS', 'Установить курс'),
        # Можно добавить другие типы действий здесь
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    action_type = models.CharField(max_length=50, choices=ACTION_TYPES, verbose_name="Тип действия")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Время действия")

    # Специфические поля для разных действий
    product = models.ForeignKey('Product', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Продукт")
    receipt = models.ForeignKey('Receipt', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Квитанция")
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Категория")
    description = models.TextField(verbose_name="Описание действия", blank=True)

    def save(self, *args, **kwargs):
        if self.action_type == 'CHANGE_PRODUCT' and not self.product:
            raise ValueError("Field 'product' must be set when action_type is 'CHANGE_PRODUCT'.")
        if self.action_type == 'CHANGE_RECEIPT' and not self.receipt:
            raise ValueError("Field 'receipt' must be set when action_type is 'CHANGE_RECEIPT'.")
        if self.action_type == 'CHANGE_DISCOUNT' and not self.category:
            raise ValueError("Field 'category' must be set when action_type is 'CHANGE_DISCOUNT'.")
        super().save(*args, **kwargs)



    def __str__(self):
        return f"{self.get_action_type_display()} - {self.user.username} - {self.timestamp}"

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
# import cv2
import numpy as np
from django.http import JsonResponse
from . models import *
from django.contrib import messages
from icecream import ic
from fuzzywuzzy import process
import qrcode
from io import BytesIO
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

# для принятия info о продуктак которые надо купить, после нажатия на купить в kassa2
from django.views.decorators.csrf import csrf_exempt
import json

# login register
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserRegistrationForm, CustomAuthenticationForm

from datetime import datetime, date
from datetime import timedelta
from calendar import monthrange
from calendar import month_name
import calendar

from django.db.models import Sum
import tablib
from django.http import HttpResponse
from django.db.models import Count

from django.utils import timezone
import pytz

from django.db.models import Q


import uuid
import getmac
import psutil
import platform




def logout_view(request):
    logout(request)
    return redirect('base_page')

def login_view(request):
    context = {}
    context['login'] = True
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('base_page')  # Замените на ваше имя URL
    else:
        form = CustomAuthenticationForm()
    context['form'] = form
    return render(request, 'shop/components/login.html', context)


# product_name product_description product_price_purchase product_price_sale product_discount product_profit product_category product_stock product_image product_qr_image product_bar_image
# add_product_name add_product_description add_product_price_purchase add_product_price_sale add_product_discount add_product_profit add_product_category add_product_stock add_product_image add_product_qr_image add_product_bar_image




# @login_required(login_url='/login/')
def add_new_product_and_generate_QRCode(request):
    context = {}

    if not request.user.is_authenticated:
        messages.error(request, 'Вы не аутентефицированы')
        context['base_page'] = True
        return render(request, 'shop/base_page.html', context)

    user_groups = request.user.groups.all()
    group_names = [group.name for group in user_groups]
    
    
    if 'adminGroup' not in group_names:
        context['base_page'] = True
        messages.error(request, 'У вас не достаточно прав')
        return render(request, 'shop/base_page.html', context)

    

    context['add_new_product_and_generate_QRCode'] = True
    context['cats'] = Category.objects.all()

    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        product_price_purchase = float(request.POST.get('product_price_purchase')) if ',' not in request.POST.get('product_price_purchase') else float(request.POST.get('product_price_purchase').replace(',', '.')) 
        # product_price_sale = float(request.POST.get('product_price_sale'))
        # price_sale_optom = float(request.POST.get('product_price_optom_sale'))
        product_price_sale = float(request.POST.get('product_price_sale')) if ',' not in request.POST.get('product_price_sale') else float(request.POST.get('product_price_sale').replace(',', '.')) 
        price_sale_optom = float(request.POST.get('product_price_optom_sale')) if ',' not in request.POST.get('product_price_optom_sale') else float(request.POST.get('product_price_optom_sale').replace(',', '.')) 

        product_category = request.POST.get('product_category')
        product_stock = float(request.POST.get('product_stock')) if request.POST.get('product_stock') != '' else 0
        code_text = request.POST.get('inputed_code_text')
        cubic_meter = request.POST.get('cubic_meter')

        context['product_name'] = product_name
        context['product_category'] = product_category

   
            

        try:
            product = Product.objects.get(name=product_name)
            action_type = 'CHANGE_PRODUCT'  # Обновление существующего продукта
            
            # Сохраняем старые значения для сравнения
            old_values = {
                'price_purchase': product.price_purchase,
                'price_sale': product.price_sale,
                'price_sale_optom': product.price_sale_optom,
                'category': product.category.name,
                'stock': product.stock,
                'code_text': product.code_text,
                'cubic_meter': product.cubic_meter,
            }
        except Product.DoesNotExist:
            product = Product()
            action_type = 'CHANGE_PRODUCT'  # Создание нового продукта
            
            # Задаем старые значения для нового продукта (пустые)
            old_values = {key: None for key in ['price_purchase', 'price_sale', 'price_sale_optom', 'category', 'stock', 'code_text', 'cubic_meter']}

        # Установка полей продукта
        product.name = product_name
        product.price_purchase = product_price_purchase
        product.price_sale = product_price_sale
        product.price_sale_optom = price_sale_optom
        product.category = Category.objects.get(name=product_category)
        product.stock = product_stock
        if cubic_meter:
            product.cubic_meter = cubic_meter


        if code_text:
            product.code_text = code_text
        product.save()

        # Составляем описание изменений
        changes = []
  
        if old_values['price_purchase'] != product_price_purchase:
            changes.append(f"Закупочная цена изменена с {old_values['price_purchase']} на {product_price_purchase}")
        if old_values['price_sale'] != product_price_sale:
            changes.append(f"Цена продажи изменена с {old_values['price_sale']} на {product_price_sale}")
        if old_values['price_sale_optom'] != price_sale_optom:
            changes.append(f"Цена продажи оптом изменена с {old_values['price_sale_optom']} на {price_sale_optom}")
        if old_values['category'] != product_category:
            changes.append(f"Категория изменена с '{old_values['category']}' на '{product_category}'")
        if old_values['stock'] != product_stock:
            changes.append(f"Запас изменен с {old_values['stock']} на {product_stock}")
        if old_values['code_text'] != code_text:
            changes.append(f"Код продукта изменен с '{old_values['code_text']}' на '{code_text}'")
        if old_values['cubic_meter'] != cubic_meter:
            changes.append(f"M3 продукта изменен с '{old_values['cubic_meter']}' на '{cubic_meter}'")

        action_description = " | ".join(changes) if changes else "Продукт сохранен без изменений."

        # Запись в журнал действий
        ActionHistory.objects.create(
            user=request.user,
            action_type=action_type,
            product=product,
            description=action_description
        )

        messages.success(request, 'Успешное сохранение')

    return render(request, 'shop/add_new_product_and_generate_QRCode.html', context)


# @login_required
def base_page(request):
    context = {}
    
    context['base_page'] = True

    return render(request, 'shop/base_page.html', context)


# @login_required
def kassa_page(request):
    context = {}

    if not request.user.is_authenticated:
        messages.error(request, 'Вы не аутентефицированы')
        return render(request, 'shop/base_page.html', context)

    context['kassa_page'] = True

    product_test = Product.objects.all()
    for product in product_test:
        if product.discount:
            product.price_after_discount = float(product.price_sale) - (float(product.price_sale) * (float(product.discount/100)))
    context['product_test'] = product_test

    if request.method == 'POST' and 'product_id_form_input' in request.POST:
        product_ids = request.POST.getlist('product_id_form_input')
        product_counts = request.POST.getlist('product_count_list')

        

        if product_ids and product_counts:

            # for pk, count in zip(product_ids, product_counts):
            #     product = Product.objects.get(pk=pk)
            #     product.stock -= int(count)
            #     product.save()

            messages.success(request, 'Покупка успешно завершена.')

        else:

            messages.error(request, 'Ошибка')


    # # Создание объекта для распознавания QR-кодов
    # detector = cv2.QRCodeDetector()

    # # Открытие камеры
    # cap = cv2.VideoCapture(0)

    # while True:
    #     # Чтение кадра с камеры
    #     ret, frame = cap.read()

    #     # Проверка, что кадр был получен
    #     if not ret:
    #         break

    #     # Распознавание QR-кода
    #     qr_data, points, _ = detector.detectAndDecode(frame)

    #     # Если QR-код был распознан
    #     if points is not None:
    #         # Если QR-код содержит данные, вывести их
    #         if qr_data:
    #             print("QR Code:", qr_data)

    #         # Рисуем рамку вокруг QR-кода
    #         points = np.int32(points).reshape(-1, 2)
    #         for i in range(len(points)):
    #             pt1 = tuple(points[i])
    #             pt2 = tuple(points[(i + 1) % len(points)])
    #             cv2.line(frame, pt1, pt2, (0, 255, 0), 3)

    #         # Отображаем текст с QR-кодом на изображении
    #         cv2.putText(frame, qr_data, (points[0][0], points[0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    #     # Отображение кадра с рамкой вокруг QR-кода
    #     cv2.imshow('QR Scanner', frame)

    #     # Завершение работы при нажатии клавиши 'q'
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break

    # # Закрытие камеры и окон
    # cap.release()
    # # cv2.destroyAllWindows()

    return render(request, 'shop/kassa_page.html', context)


# @login_required
def kassaPage2(request):
    context = {}

    if not request.user.is_authenticated:
        messages.error(request, 'Вы не аутентефицированы')
        context['base_page'] = True
        return render(request, 'shop/base_page.html', context)
    context['kassa_page2'] = True

  


    # # Получаем топ 5 продаваемых продукта
    # top5SellsProduct = Product.objects.annotate(sales_count=Count('receiptproduct')).order_by('-sales_count')[:5]
    # context['top5SellsProduct'] = top5SellsProduct

    


    # # Вывод все инфы о квитанции 
    # receipt = Receipt.objects.latest('pk')
    # print(f"Кассир: {receipt.kassir.username}")
    # print(f"Дата покупки: {receipt.created}")
    # print(f"Сумма квитанции: {receipt.total}")
    # receipt_products = ReceiptProduct.objects.filter(receipt=receipt)
    # print("Продукты в квитанции:")
    # for receipt_product in receipt_products:
    #     product_name = receipt_product.product.name  # Предполагается, что у продукта есть поле name
    #     quantity = receipt_product.quantity
    #     print(f"- {product_name}: {quantity}")


    return render(request, 'shop/kassaPage2.html', context)
    

# Это для поиска и возврата продукта 
# @login_required
def product_detail(request, product_code_data):
    ic('product_detail', product_code_data)

    # Проверяем есть ли такой qr или bar код взят с qr аппарата
    if request.headers.get('X-Source') == 'kassa2GetProduct_QR_and_Bar':

        have_product = Product.objects.filter(code_text=product_code_data).exists()
        ic(have_product)
        data = {'product': False}
        if have_product:
            product = Product.objects.get(code_text=product_code_data)
            data = {
                'product': {
                    'id': product.id, 
                    'name': product.name, 
                    'slug': product.slug, 
                    'price_purchase': product.price_purchase_manat,
                    'price_sale': product.price_sale_manat, 
                    'price_sale_optom': product.price_sale_optom_manat, 
                    'cubic_meter': product.cubic_meter, 
                    'category': product.category.name, 
                    'stock': product.stock, 
                    'code_text': product.code_text, 
                    'code_image': product.code_image.url, 
                },
            }
        return JsonResponse(data)

def product_detail_with_id(request, id):
    ic('idddddd', id)
    product = Product.objects.get(pk=id)
    data = {'product': False}
    if product:
        data = {
            'product': {
                'id': product.id, 
                'name': product.name, 
                'slug': product.slug, 
                'price_purchase': product.price_purchase_manat,
                'price_sale': product.price_sale_manat, 
                'price_sale_optom': product.price_sale_optom_manat, 
                'cubic_meter': product.cubic_meter, 
                'category': product.category.name, 
                'stock': product.stock, 
                'code_text': product.code_text, 
                'code_image': product.code_image.url, 
            },
        }
    return JsonResponse(data)

def get_product_list_from_hand_value(request, hand_value):
    ic('hand_value', hand_value)
    products = Product.objects.filter(code_text__icontains=hand_value)
    if products:
        data = {
            'products': [{
                'id': product.id, 
                'name': product.name, 
                'slug': product.slug, 
                'price_purchase': product.price_purchase_manat,
                'price_sale': product.price_sale_manat, 
                'price_sale_optom': product.price_sale_optom_manat, 
                'cubic_meter': product.cubic_meter, 
                'category': product.category.name, 
                'stock': int(product.stock), 
                'code_text': product.code_text, 
                'code_image': product.code_image.url, 
                } for product in products]
            }
    else:
        data = {
            'products': []
        }
    return JsonResponse(data)
 




# Json, suggestionsList. Возвращает список имен, совпадающих с введенными пользователем, а также отфильтрованные продукты с совпадающими именами.
# @login_required
def check_product_name(request):
    ic('tututut555')
    
    product_name = request.GET.get('product_name', None)

    all_products = Product.objects.values_list('name', flat=True)

    # Используем FuzzyWuzzy для поиска похожих названий
    matches = process.extract(product_name, all_products, limit=5)  # Получаем до 5 совпадений

    # Фильтруем по минимальному порогу схожести (например, 70)
    product_matches = [match for match in matches if match[1] >= 60]



    if len(product_matches) > 0:
        match_names = [match[0] for match in product_matches]
        products = Product.objects.filter(name__in=match_names)
        data = {
                'matches': [match[0] for match in product_matches],  # Список совпадений
                'products': [{
                    'id': product.id, 
                    'name': product.name, 
                    'price_purchase': product.price_purchase,
                    'price_sale': product.price_sale, 
                    'price_sale_optom': product.price_sale_optom,
                    'category': product.category.name, 
                    'stock': product.stock,  
                    'cubic_meter': product.cubic_meter,  
                    'code_text': product.code_text,
                    'code_image': product.code_image.url,
                    } for product in products]
            }
    else:
        data = {
            'matches': [],
            'products': []
        }


    
    return JsonResponse(data)




# Если нажал на купить то выполнить покупку
# @csrf_exempt  # Если CSRF токен не используется, можно добавить декоратор (не рекомендуется для production)
# def product_info_for_buy(request):
#     if request.method == 'POST':
#         ic('icicciciicci')
#         try:
#             # Получаем и декодируем JSON данные из запроса
#             data = json.loads(request.body)
#             if data:
#                 totalPrice = 0
#                 receipt = Receipt.objects.create(kassir=request.user, total=totalPrice)
#                 for pk, count in data.items():
#                     product = Product.objects.get(pk=pk)
#                     if product.discount:
#                         price = float(product.price_sale) - (float(product.price_sale) * (float(product.discount) / 100))
#                     else:
#                         price = float(product.price_sale)
#                     totalPrice += price * float(count)
#                     # Создайте запись в промежуточной модели ReceiptProduct
#                     ReceiptProduct.objects.create(receipt=receipt, product=product, quantity=count)
#                 # Обновите сумму квитанции
#                 receipt.total = totalPrice
#                 receipt.save()
     
#             return JsonResponse({'message': 'Data received successfully!'}, status=200)
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid data'}, status=400)
#     return JsonResponse({'error': 'Invalid request method'}, status=405)



@csrf_exempt  # Если CSRF токен не используется, можно добавить декоратор (не рекомендуется для production)
def product_info_for_buy(request):
    if request.method == 'POST':
        try:
            # Получаем и декодируем JSON данные из запроса
            data = json.loads(request.body)
            if data:
                ic('haveData', data)
                totalPrice = 0
                totalPrice_dollar = 0
                receipt = Receipt.objects.create(kassir=request.user, total=totalPrice, total_manat=totalPrice_dollar)
                for pk, countPrice in data.items():
                    count = float(countPrice['count'])
                    price = float(countPrice['price'])
                    price_dollar = float(countPrice['price']) / float(Kurs.objects.first().kurs)
                    product = Product.objects.get(pk=pk)
                    totalPrice += price * count
                    totalPrice_dollar += price_dollar * count

                    # Умещение количества товара на складе
                    if product.stock >= count:  # Проверяем, достаточно ли товара на складе
                        product.stock = float(product.stock) -  count  # Уменьшаем количество на складе
                        product.save()  # Сохраняем обновленный продукт
                        # Создайте запись в промежуточной модели ReceiptProduct
                        ReceiptProduct.objects.create(
                            receipt=receipt, 
                            product=product, 
                            quantity=count,

                            price_purchase=product.price_purchase,
                            price_sale=price_dollar,

                            price_purchase_manat=product.price_purchase_manat,
                            price_sale_manat=price,

                            profit= price_dollar - float(product.price_purchase),
                            profit_manat = price - float(product.price_purchase_manat),

                            product_name=product.name,
                            product_slug=product.slug
                            )
                    else:
                        return JsonResponse({'error': f'Недостаточно товара: {product.name}'}, status=400)

                # Обновите сумму квитанции
                receipt.total = totalPrice_dollar
                receipt.total_manat = totalPrice
                receipt.save()
            return JsonResponse({'message': 'Data received successfully!'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid data'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)



def receipts(request):
    context = {}

    if not request.user.is_authenticated:
        messages.error(request, 'Вы не аутентефицированы')
        context['base_page'] = True
        return render(request, 'shop/base_page.html', context)

    context['receipts'] = True
    user_groups = request.user.groups.all()
    group_names = [group.name for group in user_groups]

    users = User.objects.all()
    users_list = []
    for user in users:
        users_list.append(user.username)
    context['kassirs'] = users_list


    # Если отменил квитанцию (возврат покупка)
    if request.method == 'POST' and 'changeReceiptPK' in request.POST:
        
        changeReceiptPK = request.POST.get('changeReceiptPK')
        receipt = get_object_or_404(Receipt, pk=changeReceiptPK)

        if 'adminGroup' not in user_groups and not request.user.is_superuser:
            receiptFilter = Receipt.objects.filter(pk=changeReceiptPK)
            context['receipts'] = receiptFilter
            messages.error(request, 'У вас нет прав для отмены квитанции')
        else:

            receipt_products = ReceiptProduct.objects.filter(receipt=receipt)
            product_details = []
            
            for rp in receipt_products:
                # Обновляем запасы
                Product.objects.filter(pk=rp.product.pk).update(stock=F('stock') + rp.quantity)
                # Составляем список продуктов с количеством
                product_details.append(f"{rp.product.name} (Количество: {rp.quantity})")
            
            # Отмечаем квитанцию как измененную
            receipt.changed = True
            receipt.save()

            # Составляем полное описание для журнала действий
            products_description = ", ".join(product_details)
            action_description = f'Квитанция отменена. Продукты: {products_description}.'

            # Запись в журнал действий
            ActionHistory.objects.create(
                user=request.user,
                action_type='CHANGE_RECEIPT',
                receipt=receipt,
                description=action_description
            )

            messages.success(request, "Успешная отмена квитанции")

            receiptFilter = Receipt.objects.filter(pk=changeReceiptPK)
            context['receipts'] = receiptFilter

    # если нажал на скачать excel receipts
    elif request.method == 'POST' and 'download_excel' in request.POST:
        headers = (
            "Product",
            "Kolichestwo",

            "1 alnan TMT",
            "1 alnan $",
            "1 satylan TMT",
            "1 satylan $",
            "1 girdeji TMT", 
            "1 girdeji $", 

            "umumy alnan TMT",
            "umumy alnan $",

            "umumy satylan TMT", 
            "umumy satylan $", 
            
            "umumy girdeji TMT", 
            "umumy girdeji $", 

            "Kassir", 
            "Changed", 
            "Created"
            )
        dataset = []
        dataset = tablib.Dataset(headers=headers)

        dateStart = request.POST.get('dateStart')
        dateEnd = request.POST.get('dateEnd')
     
        kassir = request.POST.get('kassir')
        changeReceiptSelect = request.POST.get('changeReceiptSelect')
        context['dateStart'] = dateStart
        context['dateEnd'] = dateEnd
        context['kassir'] = kassir
        context['changeReceiptSelect'] = changeReceiptSelect

        if dateStart:
            if kassir:
                if changeReceiptSelect == 'dontChanged':
                    receipts = Receipt.objects.filter(created__range=[dateStart, dateEnd], kassir__username=kassir, changed=False).order_by('-created')
                elif changeReceiptSelect == 'changed':
                    receipts = Receipt.objects.filter(created__range=[dateStart, dateEnd], kassir__username=kassir, changed=True).order_by('-created')
                else:
                    receipts = Receipt.objects.filter(created__range=[dateStart, dateEnd], kassir__username=kassir).order_by('-created')
            else:
                if changeReceiptSelect == 'dontChanged':
                    receipts = Receipt.objects.filter(created__range=[dateStart, dateEnd], changed=False).order_by('-created')
                elif changeReceiptSelect == 'changed':
                    receipts = Receipt.objects.filter(created__range=[dateStart, dateEnd], changed=True).order_by('-created')
                else:
                    receipts = Receipt.objects.filter(created__range=[dateStart, dateEnd]).order_by('-created')
        else:
            # now = datetime.now()
            now = timezone.now() 
            dateStart = now.replace(day=1)
            last_day = monthrange(now.year, now.month)[1]
            dateEnd = now.replace(day=last_day)
            receipts = Receipt.objects.filter(created__range=[dateStart, dateEnd]).order_by('-created')
            dateStart = dateStart.strftime('%Y-%m-%d')
            dateEnd = dateEnd.strftime('%Y-%m-%d')
    
        context['receipts'] = receipts

        for r in receipts:

            changed = ''
            if r.changed:
                changed = 'Отменено'

            rp = r.receiptproduct_set.all()  # Получаем все продукты в квитанции
            totalPrice = r.total
            kassir = r.kassir.username

            # Преобразуем время в локальное (UTC+5 для Туркменистана)
            local_created_time = timezone.localtime(r.created, timezone=pytz.timezone('Asia/Ashgabat'))
            # created = r.created.strftime('%Y-%m-%d %H:%M:%S') + f".{int(r.created.microsecond / 1000):03d}"

            # Форматируем время
            created = local_created_time.strftime('%Y-%m-%d %H:%M:%S') + f".{int(local_created_time.microsecond / 1000):03d}"
        
            # headers = (
            #     "Product",
            #     "Kolichestwo",

            #     "1 alnan TMT",
            #     "1 alnan $",
            #     "1 satylan TMT",
            #     "1 satylan $",
            #     "1 girdeji TMT", 
            #     "1 girdeji $", 

            #     "umumy alnan TMT",
            #     "umumy alnan $",

            #     "umumy satylan TMT", 
            #     "umumy satylan $", 

            #     "umumy girdeji TMT", 
            #     "umumy girdeji $", 

            #     "Kassir", 
            #     "Changed", 
            #     "Created"
            #     )

            for product in rp:
                profit = 0
                if product.quantity:
                    profit = product.profit
                dataset.append((
                    product.product_name,
                    product.quantity,

                    product.price_purchase_manat, # "1 alnan TMT",
                    product.price_purchase, # "1 alnan $",

                    product.price_sale_manat, # "1 satylan TMT",
                    product.price_sale,  # ""1 satylan $",,

                    float(product.price_sale_manat) - float(product.price_purchase_manat), # "1 sany girdeji manat",
                    float(product.price_sale) - float(product.price_purchase), # "1 sany girdeji Q",

                   

                    float(product.price_purchase_manat) * float(product.quantity), # "umumy alnan TMT",
                    float(product.price_purchase) * float(product.quantity), # "umumy alnan $",


                    
                    float(product.price_sale_manat) * float(product.quantity), # "umumy Baha manat", 
                    float(product.price_sale) * float(product.quantity), #  "umumy Baha Q",
                    
                    (float(product.price_sale_manat) - float(product.price_purchase_manat)) * float(product.quantity), # "umumy girdeji manat", 
                    (float(product.price_sale) - float(product.price_purchase)) * float(product.quantity), # "umumy girdeji Q", 
                   
                    
                    

                    kassir,  # Имя кассира
                    changed,
                    str(created)

                ))

        # response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
        response = HttpResponse(dataset.export('xlsx'), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f"attachment; filename= Recipts_{str(dateStart)} {str(dateEnd)}.xlsx"
        return response

    else:
        # Вывод все инфы о квитанции 
        receipts = Receipt.objects.all().order_by('-created')[:10]
        kassir = ''
        if request.method =='POST':
            dateStart = request.POST.get('dateStart')
            dateEnd = request.POST.get('dateEnd')


            kassir = request.POST.get('kassir')
            changeReceiptSelect = request.POST.get('changeReceiptSelect')
            context['dateStart'] = dateStart
            context['dateEnd'] = dateEnd

            context['kassir'] = kassir
            context['changeReceiptSelect'] = changeReceiptSelect

            if kassir:
                if changeReceiptSelect == 'dontChanged':
                    receipts = Receipt.objects.filter(created__range=[dateStart, dateEnd], kassir__username=kassir, changed=False).order_by('-created')
                elif changeReceiptSelect == 'changed':
                    receipts = Receipt.objects.filter(created__range=[dateStart, dateEnd], kassir__username=kassir, changed=True).order_by('-created')
                else:
                    receipts = Receipt.objects.filter(created__range=[dateStart, dateEnd], kassir__username=kassir).order_by('-created')
            else:
                if changeReceiptSelect == 'dontChanged':
                    receipts = Receipt.objects.filter(created__range=[dateStart, dateEnd], changed=False).order_by('-created')
                elif changeReceiptSelect == 'changed':
                    receipts = Receipt.objects.filter(created__range=[dateStart, dateEnd], changed=True).order_by('-created')
                else:
                    receipts = Receipt.objects.filter(created__range=[dateStart, dateEnd]).order_by('-created')
    
        context['receipts'] = receipts
     


        


    return render(request, 'shop/receipts.html', context)


def otchyot(request):
    context = {}

    if not request.user.is_authenticated:
        messages.error(request, 'Вы не аутентефицированы')
        context['base_page'] = True
        return render(request, 'shop/base_page.html', context)

    context['otchyot'] = True

    products = Product.objects.all()

    users = User.objects.all()
    users_list = []
    for user in users:
        users_list.append(user.username)
    context['kassirs'] = users_list

    context['price_sale2'] = []
    context['price_profit'] = []
    context['price_purchase2'] = []
    context['days_difference'] = []

    context['month_list'] = []
    context['month_purchases'] = []
    context['month_sales'] = []
    context['month_profits'] = []

    context['year_list'] = []
    context['yearly_purchases'] = []
    context['yearly_sales'] = []
    context['yearly_profits'] = []


    if request.method == 'POST':
        dateStart = request.POST.get('dateStart')
        dateEnd = request.POST.get('dateEnd')
        kassir = request.POST.get('kassir')
        context['dateStart'] = dateStart
        context['dateEnd'] = dateEnd
        context['kassir'] = kassir


        if kassir:
            receipts = Receipt.objects.filter(created__range=[dateStart, dateEnd], kassir__username=kassir, changed=False).order_by('-created')
        else:
            receipts = Receipt.objects.filter(created__range=[dateStart, dateEnd], changed=False).order_by('-created')
        context['receipts2'] = receipts

        total_sale = 0
        total_purchase = 0
        total_profit = 0
        for r in receipts:
            for rp in r.receiptproduct_set.all():
                total_sale += rp.price_sale * rp.quantity
                total_purchase += rp.price_purchase * rp.quantity
                total_profit += rp.profit * rp.quantity

        context['total_sale'] = total_sale
        context['total_purchase'] = total_purchase
        context['total_profit'] = total_profit



       
        # start_month = int(dateStart[5:7])
        # start_year = int(dateStart[:4])
        # end_month = int(dateEnd[5:7])
        # end_year = int(dateEnd[:4])
 
        # Это заменил на нижнее так как есть какаято ошибка с использованием наивного времени в сочетании с поддержкой временных зон в Django. Код работает но есть небольшой дефект который может привести к непредсказуемым ошибкам
        # # Преобразуем строки в объекты datetime
        # date_format = '%Y-%m-%d'  # Измените формат в зависимости от формата ваших дат
        # date_start = datetime.strptime(dateStart, date_format)
        # date_end = datetime.strptime(dateEnd, date_format)

        # Преобразуем строки в объекты datetime
        date_format = '%Y-%m-%d'
        date_start = timezone.make_aware(datetime.strptime(dateStart, date_format))
        date_end = timezone.make_aware(datetime.strptime(dateEnd, date_format))

         # Вычисляем разницу в месяцах
        month_difference = (date_end.year - date_start.year) * 12 + date_end.month - date_start.month
        
        # Если нужно, чтобы разница была выражена как положительное число
        month_difference = abs(month_difference)
        
        
        # Вычисление разницы между датами
        delta = date_end - date_start

        # Получение количества дней
        days_difference = delta.days
        # количество дней в дате старт (а то при сортировке по датам с 01.10.2024 по 01.11.2024 сортирует дни с 1 по 29, а 30 день не показывает)
        days_in_month = calendar.monthrange(date_start.year, date_start.month)[1]


        

        ###############################################################################################################################################################################################
        # Если нужен график за месяц (выводим отчет по дням)
        if month_difference == 0 or days_difference <= days_in_month:
            # Вычисляем разницу между датами
            delta = date_end - date_start
            days_difference = delta.days
        
            # Список для хранения всех дней между двумя датами
            days_difference_list = []
            # Используем цикл для добавления дней в список
            current_date = date_start
            while current_date < date_end:
                days_difference_list.append(current_date.day)  # добавляем день как int
                current_date += timedelta(days=1)  # переходим к следующему дню

            # Сохранение в контексте
            context['days_difference'] = days_difference_list


            if kassir:
                receipts = Receipt.objects.filter(created__range=[dateStart, dateEnd], kassir__username=kassir, changed=False).order_by('-created')
            else:
                receipts = Receipt.objects.filter(created__range=[dateStart, dateEnd], changed=False).order_by('-created')

            context['receipts2'] = receipts

            price_sale2 = []
            price_profit = []
            price_purchase2 = []

            # Проход по каждому дню в диапазоне
            current_date = date_start
            while current_date <= date_end:
                # Устанавливаем следующий день для фильтрации по диапазону
                next_day = current_date + timedelta(days=1)
                
                if kassir:
                    # Фильтруем квитанции для конкретного дня и кассира
                    receipts = Receipt.objects.filter(
                        created__range=[current_date, next_day],
                        kassir__username=kassir,
                        changed=False
                    )
                else:
                    # Фильтруем квитанции для конкретного дня без указания кассира
                    receipts = Receipt.objects.filter(
                        created__range=[current_date, next_day],
                        changed=False
                    )
                
                # Суммируем все покупки за текущий день
                total_sale_for_day = receipts.aggregate(total=models.Sum('total'))['total'] or 0
                # Добавляем результат в список
                price_sale2.append(float(total_sale_for_day))

                # Рассчитываем прибыль за текущий день START
                total_profit_for_day = 0
                for receipt in receipts:
                    receipt_products = ReceiptProduct.objects.filter(receipt=receipt)
                    for rp in receipt_products:
                        total_profit_for_day += rp.profit * rp.quantity
                price_profit.append(float(total_profit_for_day))
                # Рассчитываем прибыль за текущий день END

                # Рассчитываем Цену покупка за текущий день START
                total_pursache_for_day = 0
                for receipt in receipts:
                    receipt_products = ReceiptProduct.objects.filter(receipt=receipt)
                    for rp in receipt_products:
                        total_pursache_for_day += rp.price_purchase * rp.quantity
                price_purchase2.append(float(total_pursache_for_day))
                # Рассчитываем Цену покупка за текущий день END
                
                # Переходим к следующему дню
                current_date = next_day
            context['price_sale2'] = price_sale2
            context['price_profit'] = price_profit
            context['price_purchase2'] = price_purchase2


            total_sale = 0
            total_purchase = 0
            total_profit = 0
            for i in price_sale2:
                total_sale += i
            for i in price_profit:
                total_purchase += i
            for i in price_purchase2:
                total_profit += i
            context['total_sale'] = total_sale
            context['total_purchase'] = total_purchase
            context['total_profit'] = total_profit
        
                
        ###############################################################################################################################################################################################
        # выводим график по месяцам
        elif month_difference > 0 and month_difference < 13:
            # ic('график по месяцам')

            # Словарь с переводом месяцев
            month_translation = {
                "January": "Январь",
                "February": "Февраль",
                "March": "Март",
                "April": "Апрель",
                "May": "Май",
                "June": "Июнь",
                "July": "Июль",
                "August": "Август",
                "September": "Сентябрь",
                "October": "Октябрь",
                "November": "Ноябрь",
                "December": "Декабрь"
            }

            def get_month_range(date_start, date_end):
                """
                Возвращает список месяцев между двумя датами.
                """
          
                start_date = datetime.strptime(date_start, '%Y-%m-%d')
                end_date = datetime.strptime(date_end, '%Y-%m-%d')
                
                month_list = []
                current_date = start_date
                while current_date <= end_date:
                    month_list.append(month_name[current_date.month])  # Получаем название месяца
                    # Переход на следующий месяц
                    if current_date.month == 12:
                        current_date = current_date.replace(year=current_date.year + 1, month=1)
                    else:
                        current_date = current_date.replace(month=current_date.month + 1)
                return month_list


            def get_financial_data(date_start, date_end, kassir=None):
                """
                Возвращает списки покупок, продаж и прибыли по месяцам в заданном диапазоне.
                """
            
      
                start_date = datetime.strptime(date_start, '%Y-%m-%d')
                end_date = datetime.strptime(date_end, '%Y-%m-%d')
       


                # Получаем список месяцев
                month_list = get_month_range(date_start, date_end)
              

                # Агрегация данных
                purchases = []
                sales = []
                profits = []

                # Определение диапазона месяцев
                # month_range = range(start_date.month, end_date.month + 1)
             
                # Создание списка месяцев
                if start_date.month <= end_date.month:
                    month_range = list(range(start_date.month, end_date.month + 1))
                else:
                    month_range = list(range(start_date.month, 13)) + list(range(1, end_date.month + 1))

                # print(month_range)  # Вывод: [11, 12, 1, 2]
             
                


                if kassir:
                    last_month = 0
                    get_year = 0   
                    for month in month_range:
                        if month < last_month:
                            next_yaer = start_date.year + 1
                        else:
                            last_month = month
                            next_yaer = start_date.year
                        monthly_data = ReceiptProduct.objects.filter(
                            receipt__created__year=next_yaer,
                            receipt__created__month=month,
                            receipt__kassir__username=kassir,
                            receipt__changed=False
                        ).annotate(
                            total_price_sale=F('price_sale') * F('quantity'),
                            total_price_purchase=F('price_purchase') * F('quantity'),
                            total_price_profit=F('profit') * F('quantity')
                        ).aggregate(
                            total_purchase=Sum('total_price_purchase'),
                            price_sale=Sum('total_price_sale'),
                            total_profit=Sum('total_price_profit')
                        )

                        # Добавляем данные в соответствующие списки
                        purchases.append(float(monthly_data['total_purchase']) if monthly_data['total_purchase'] is not None else 0)
                        sales.append(float(monthly_data['price_sale']) if monthly_data['price_sale'] is not None else 0)
                        profits.append(float(monthly_data['total_profit']) if monthly_data['total_profit'] is not None else 0)

                    

                else:

                    last_month = 0
                    get_year = 0
                    

                    for month in month_range:
                        if month < last_month:
                            next_yaer = start_date.year + 1
                        else:
                            last_month = month
                            next_yaer = start_date.year
                        
                      

                        monthly_data = ReceiptProduct.objects.filter(
                            receipt__created__year=next_yaer,
                            receipt__created__month=month,
                            receipt__changed=False
                        ).annotate(
                            total_price_sale=F('price_sale') * F('quantity'),
                            total_price_purchase=F('price_purchase') * F('quantity'),
                            total_price_profit=F('profit') * F('quantity')
                        ).aggregate(
                            total_purchase=Sum('total_price_purchase'),
                            price_sale=Sum('total_price_sale'),
                            total_profit=Sum('total_price_profit')
                        )

                 
                        
                        # Добавляем данные в соответствующие списки
                        purchases.append(float(monthly_data['total_purchase']) if monthly_data['total_purchase'] is not None else 0)
                        sales.append(float(monthly_data['price_sale']) if monthly_data['price_sale'] is not None else 0)
                        profits.append(float(monthly_data['total_profit']) if monthly_data['total_profit'] is not None else 0)

                    
                      
                
                return month_list, purchases, sales, profits


            month_list, month_purchases, month_sales, month_profits = get_financial_data(dateStart, dateEnd, kassir)

            months_in_russian = [month_translation[month] for month in month_list]
            print(f"Месяцы: {months_in_russian}")
            print(f"Цены покупок по месяцам: {month_purchases}")
            print(f"Цены продаж по месяцам: {month_sales}")
            print(f"Прибыль по месяцам: {month_profits}")

            context['month_list'] = months_in_russian
            context['month_purchases'] = month_purchases
            context['month_sales'] = month_sales
            context['month_profits'] = month_profits

            total_sale = 0
            total_purchase = 0
            total_profit = 0
            for i in month_sales:
                total_sale += i
            for i in month_profits:
                total_purchase += i
            for i in month_purchases:
                total_profit += i
            context['total_sale'] = total_sale
            context['total_purchase'] = total_purchase
            context['total_profit'] = total_profit


        
                    
        # График по годам
        else:
            ic('график по годам')
            ic('cacacaacca year', kassir)
            def get_year_range(date_start, date_end):
                """
                Возвращает список лет между двумя датами.
                """
                start_date = datetime.strptime(date_start, '%Y-%m-%d')
                end_date = datetime.strptime(date_end, '%Y-%m-%d')
                
                year_list = []
                current_year = start_date.year
                
                while current_year <= end_date.year:
                    year_list.append(str(current_year))  # Сохраняем год как строку
                    current_year += 1
                
                return year_list

            def get_annual_financial_data(date_start, date_end, kassir=None):
                """
                Возвращает списки покупок, продаж и прибыли по годам в заданном диапазоне.
                """
                start_date = datetime.strptime(date_start, '%Y-%m-%d')
                end_date = datetime.strptime(date_end, '%Y-%m-%d')

                year_list = get_year_range(date_start, date_end)

                yearly_purchases = []
                yearly_sales = []
                yearly_profits = []

                # Определяем диапазон лет
                year_range = range(start_date.year, end_date.year + 1)

                if kassir:
                    for year in year_range:
                        yearly_data = ReceiptProduct.objects.filter(
                            receipt__created__year=year,
                            receipt__changed=False,
                            receipt__kassir__username=kassir,
                        ).annotate(
                            total_price_sale=F('price_sale') * F('quantity'),
                            total_price_purchase=F('price_purchase') * F('quantity'),
                            total_price_profit=F('profit') * F('quantity')
                        ).aggregate(
                            total_purchase=Sum('total_price_purchase'),
                            price_sale=Sum('total_price_sale'),
                            total_profit=Sum('total_price_profit')
                        )

                        yearly_purchases.append(float(yearly_data['total_purchase']) if yearly_data['total_purchase'] is not None else 0)
                        yearly_sales.append(float(yearly_data['price_sale']) if yearly_data['price_sale'] is not None else 0)
                        yearly_profits.append(float(yearly_data['total_profit']) if yearly_data['total_profit'] is not None else 0)
                else:
                    for year in year_range:
                        yearly_data = ReceiptProduct.objects.filter(
                            receipt__created__year=year,
                            receipt__changed=False
                        ).annotate(
                            total_price_sale=F('price_sale') * F('quantity'),
                            total_price_purchase=F('price_purchase') * F('quantity'),
                            total_price_profit=F('profit') * F('quantity')
                        ).aggregate(
                            total_purchase=Sum('total_price_purchase'),
                            price_sale=Sum('total_price_sale'),
                            total_profit=Sum('total_price_profit')
                        )

                        yearly_purchases.append(float(yearly_data['total_purchase']) if yearly_data['total_purchase'] is not None else 0)
                        yearly_sales.append(float(yearly_data['price_sale']) if yearly_data['price_sale'] is not None else 0)
                        yearly_profits.append(float(yearly_data['total_profit']) if yearly_data['total_profit'] is not None else 0)

                return year_list, yearly_purchases, yearly_sales, yearly_profits

            # Вызов функции для получения финансовых данных по годам
            year_list, yearly_purchases, yearly_sales, yearly_profits = get_annual_financial_data(dateStart, dateEnd, kassir)

            context['year_list'] = year_list
            context['yearly_purchases'] = yearly_purchases
            context['yearly_sales'] = yearly_sales
            context['yearly_profits'] = yearly_profits



        


    
        if 'download_excel' in request.POST:
            headers = (
                "Product", 
                "1ps price", 
                "1ps profit", 
                "Quantity", 
                "total price", 
                "total profit", 
                "Kassir", 
                "Changed", 
                "Created"
            )
            
            # Создание нового дата-сета
            dataset = tablib.Dataset(headers=headers)

            dateStart = request.POST.get('dateStart')
            dateEnd = request.POST.get('dateEnd')
            kassir = request.POST.get('kassir')
            changeReceiptSelect = request.POST.get('changeReceiptSelect')
            ic(changeReceiptSelect)
            context['dateStart'] = dateStart
            context['dateEnd'] = dateEnd
            context['kassir'] = kassir
            context['changeReceiptSelect'] = changeReceiptSelect

            if dateStart:
                if kassir:
                    # if changeReceiptSelect == 'dontChanged':
                    receipts = Receipt.objects.filter(created__range=[dateStart, dateEnd], kassir__username=kassir, changed=False).order_by('-created')
                    # elif changeReceiptSelect == 'changed':
                    #     receipts = Receipt.objects.filter(created__range=[dateStart, dateEnd], kassir__username=kassir, changed=True).order_by('-created')
                    # else:
                    #     receipts = Receipt.objects.filter(created__range=[dateStart, dateEnd], kassir__username=kassir).order_by('-created')
                else:
                    # if changeReceiptSelect == 'dontChanged':
                    receipts = Receipt.objects.filter(created__range=[dateStart, dateEnd], changed=False).order_by('-created')
                    # elif changeReceiptSelect == 'changed':
                    #     receipts = Receipt.objects.filter(created__range=[dateStart, dateEnd], changed=True).order_by('-created')
                    # else:
                    #     receipts = Receipt.objects.filter(created__range=[dateStart, dateEnd]).order_by('-created')
            else:
                now = datetime.now()
                dateStart = now.replace(day=1)
                last_day = monthrange(now.year, now.month)[1]
                dateEnd = now.replace(day=last_day)
                receipts = Receipt.objects.filter(created__range=[dateStart, dateEnd]).order_by('-created')
                dateStart = dateStart.strftime('%Y-%m-%d')
                dateEnd = dateEnd.strftime('%Y-%m-%d')

            context['receipts'] = receipts

            for r in receipts:
                changed = 'Отменено' if r.changed else ''  # Используем тернарный оператор для упрощения
                rp = r.receiptproduct_set.all()  # Получаем все продукты в квитанции
                kassir_username = r.kassir.username
                # created = r.created.strftime('%Y-%m-%d %H:%M:%S') + f".{int(r.created.microsecond / 1000):03d}"

                # Преобразуем время в локальное (UTC+5 для Туркменистана)
                local_created_time = timezone.localtime(r.created, timezone=pytz.timezone('Asia/Ashgabat'))
                # created = r.created.strftime('%Y-%m-%d %H:%M:%S') + f".{int(r.created.microsecond / 1000):03d}"

                # Форматируем время
                created = local_created_time.strftime('%Y-%m-%d %H:%M:%S') + f".{int(local_created_time.microsecond / 1000):03d}"

                for product in rp:
                    ic(product)  # Вывод продукта для отладки
                    dataset.append((
                        product.product.name,
                        product.price_sale,  # Используем цену из ReceiptProduct
                        product.profit,  # Используем прибыль из ReceiptProduct
                        product.quantity,  # Количество продукта
                        float(product.price_sale) * product.quantity,  # Общая сумма по продукту
                        float(product.quantity) * float(product.profit),  # Подсчет прибыли по продукту
                        kassir_username,  # Имя кассира
                        changed,
                        str(created)  # Дата создания квитанции
                    ))

            # response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
            response = HttpResponse(dataset.export('xlsx'), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f"attachment; filename=Receipts_{str(dateStart)}_{str(dateEnd)}.xlsx"
            return response

    return render(request, 'shop/otchyot.html', context)


def stock(request):
    context = {}

    if not request.user.is_authenticated:
        messages.error(request, 'Вы не аутентефицированы')
        context['base_page'] = True
        return render(request, 'shop/base_page.html', context)

    context['stock'] = True

    

    name = request.GET.get('name')
    count = request.GET.get('count')
    context['name'] = name
    context['count'] = count

    if name:
        if count:
            products_list = Product.objects.filter(name__icontains=name, stock=count).order_by('stock')
        else:
            products_list = Product.objects.filter(name__icontains=name).order_by('stock')
    else:
        if count:
            products_list = Product.objects.filter(stock=count).order_by('stock')
        else:
            products_list = Product.objects.all().order_by('stock')

    lenProducts = len(products_list)

    total_purchase = 0
    for p in products_list:
        total_purchase += float(p.stock) * float(p.price_purchase)
        p.count_multyply_purchase = float(p.stock) * float(p.price_purchase)

    paginator = Paginator(products_list, 25)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    context['products'] = products
    context['productsAll'] = products_list
    context['total_purchase'] = total_purchase
    context['lenProducts'] = lenProducts

    # # Скачать excel
    # if request.method == 'POST' and 'download_excel' in request.POST:
    #     headers = ("Product", "Prodaja", "Pokupka", "Kolichestwo", "Kubic metr", "Summa pokupki")
    #     data = []
    #     data = tablib.Dataset(*data, headers=headers)

    #     for p in products_list:
    #         total_purchase = float(p.stock) * float(p.price_purchase)
    #         data.append((p.name, p.price_sale, p.price_purchase, p.stock, p.cubic_meter, total_purchase))


    #     current_date = str(date.today())
    #     response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
    #     response['Content-Disposition'] = f"attachment; filename= Products_{current_date}.xlsx"
    #     return response

    if request.method == 'POST' and 'download_excel' in request.POST:
        headers = ("Product", "Pokupka", "Kolichestwo", "Kubic metr", "Summa")
        
        # Создаем Dataset с заголовками
        dataset = tablib.Dataset(headers=headers)

        for p in products_list:
            total_purchase = float(p.stock) * float(p.price_purchase)
            dataset.append((p.name, p.price_purchase, p.stock, p.cubic_meter, total_purchase))

        # Экспортируем данные в формат xlsx
        current_date = str(date.today())
        response = HttpResponse(dataset.export('xlsx'), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=Products_{current_date}.xlsx'
        return response




    return render(request, 'shop/stock.html', context)

    
def set_discount(request):
    context = {}

    if not request.user.is_authenticated:
        messages.error(request, 'Вы не аутентефицированы')
        context['base_page'] = True
        return render(request, 'shop/base_page.html', context)

    user_groups = request.user.groups.all()
    group_names = [group.name for group in user_groups]
    if 'adminGroup' not in group_names and not request.user.is_superuser:
        context['base_page'] = True
        messages.error(request, 'У вас не достаточно прав')
        return render(request, 'shop/base_page.html', context)

    context['set_discount'] = True

    cats = list(Category.objects.values_list('name', flat=True))
    context['cats'] = cats

    if request.method == 'POST':
        category = request.POST.get('category')
        discount = request.POST.get('discount')

        if category and discount:
            products = Product.objects.filter(category__name=category)
            cat = Category.objects.get(name=category)

            for product in products:
                product.discount = int(discount)
                product.save()
                

            # Запись в журнал действий
            ActionHistory.objects.create(
                user=request.user,
                action_type='CHANGE_DISCOUNT',
                category=cat,
                description=f'Изменение скидки на {discount}% для категории {category}'
                )

            
            messages.success(request, f'Скидка {discount}% на все товары категории {category}')

        else:

            messages.error(request, f'Заполните все поля')
 
    return render(request, 'shop/set_discount.html', context)


# def action_history(request):
#     context = {}

#     if not request.user.is_authenticated:
#         messages.error(request, 'Вы не аутентефицированы')
#         context['base_page'] = True
#         return render(request, 'shop/base_page.html', context)

#     context['action_history'] = True

#     types = [action[1] for action in ActionHistory.ACTION_TYPES]
#     types_dict = {}

#     for act in ActionHistory.ACTION_TYPES:
#         types_dict[act[1]] = act[0]

#     context['types'] = types


#     # ################################################################################################
#     # ################################################################################################
#     # def get_unique_id():
#     #     # Получение MAC-адреса
#     #     mac_address = getmac.get_mac_address()  # Вернет MAC-адрес или None

#     #     # Генерация UUID на основе имени сети
#     #     uuid_from_mac = str(uuid.uuid5(uuid.NAMESPACE_DNS, mac_address))

#     #     # Собираем информацию о системе
#     #     system_info = platform.uname()  # Получает информацию о системе
#     #     system_name = system_info.node  # Имя компьютера

#     #     # Получение серийного номера диска (если доступно)
#     #     serial_number = ''
#     #     try:
#     #         # Получаем информацию о жестких дисках
#     #         partitions = psutil.disk_partitions()
#     #         for partition in partitions:
#     #             partition_info = psutil.disk_usage(partition.mountpoint)
#     #             serial_number = partition_info.total  # Просто пример, реальный серийный номер обычно требует отдельных библиотек.
#     #     except Exception as e:
#     #         print(f'Ошибка получения серийного номера: {str(e)}')

#     #     # Составляем уникальный идентификатор
#     #     unique_id = f"{mac_address}-{uuid_from_mac}-{system_name}-{serial_number}"

#     #     return unique_id

#     # mac_address = getmac.get_mac_address()
#     # uuid_from_mac = str(uuid.uuid5(uuid.NAMESPACE_DNS, mac_address))
#     # system_info = platform.uname()  # Получает информацию о системе
#     # system_name = system_info.node  # Имя компьютера
#     # serial_number = ''
#     # try:
#     #     # Получаем информацию о жестких дисках
#     #     partitions = psutil.disk_partitions()
#     #     for partition in partitions:
#     #         partition_info = psutil.disk_usage(partition.mountpoint)
#     #         serial_number = partition_info.total  # Просто пример, реальный серийный номер обычно требует отдельных библиотек.
#     # except Exception as e:
#     #     print(f'Ошибка получения серийного номера: {str(e)}')

#     # ic(mac_address)
#     # ic(uuid_from_mac)
#     # ic(system_info)
#     # ic(system_name)
#     # ic(serial_number)
#     # ################################################################################################
#     # ################################################################################################


    

    

#     usernames = [user.username for user in User.objects.all()]
#     context['usernames'] = usernames

#     if request.method == 'POST':
#         user_name = request.POST.get('user_name')
#         action = request.POST.get('action')
#         description = request.POST.get('description')
#         dateStart = request.POST.get('dateStart')
#         dateEnd = request.POST.get('dateEnd')

#         context['dateStart'] = dateStart
#         context['dateEnd'] = dateEnd
#         context['user_name_choosed'] = user_name
#         context['action_choosed'] = action
#         context['description'] = description


#         # if user_name and action:
#         #     action_history = ActionHistory.objects.filter(user__username = user_name, action_type=types_dict[action])
#         #     ic(action_history)
#         #     context['action_history'] = action_history

        
#         if action == 'sells':
#             if user_name:
#                 receipts_list = Receipt.objects.filter(kassir__username = user_name, created__range=[dateStart, dateEnd])
#             else:
#                 receipts_list = Receipt.objects.filter(created__range=[dateStart, dateEnd])

#             context['receipts_list'] = receipts_list
#             if len(receipts_list) == 0:
#                 context['receipts_none'] = True

#         else:
#             # Получаем список объектов на основе фильтрации
#             filters = {}

#             # Добавляем фильтры на основе заполненных значений
#             if dateStart and dateEnd:
#                 filters['timestamp__range'] = [dateStart, dateEnd]

#             if user_name:
#                 filters['user__username'] = user_name

#             if action and action != "":  # Проверяем, что action не пустой
#                 filters['action_type'] = types_dict.get(action)

#             action_history = ActionHistory.objects.filter(**filters).order_by("-timestamp")[:500]
#             context['action_list'] = action_history
#             # Если у вас есть description, вы можете добавить его фильтр
#             if description:
#                 context['action_list'] = action_history.filter(description__icontains=description).order_by("-timestamp")[:500]

 
#     return render(request, 'shop/action_history.html', context)

def action_history(request):
    context = {}

    if not request.user.is_authenticated:
        messages.error(request, 'Вы не аутентифицированы')
        context['base_page'] = True
        return render(request, 'shop/base_page.html', context)

    context['action_history'] = True

    types = [action[1] for action in ActionHistory.ACTION_TYPES]
    types_dict = {action[1]: action[0] for action in ActionHistory.ACTION_TYPES}
    context['types'] = types

    usernames = [user.username for user in User.objects.all()]
    context['usernames'] = usernames

    user_name = request.GET.get('user_name')
    action = request.GET.get('action')
    description = request.GET.get('description')
    dateStart = request.GET.get('dateStart')
    dateEnd = request.GET.get('dateEnd')

    context['dateStart'] = dateStart
    context['dateEnd'] = dateEnd
    context['user_name_choosed'] = user_name
    context['action_choosed'] = action
    context['description'] = description

    if action == 'sells':
        if user_name:
            receipts_list = Receipt.objects.filter(kassir__username=user_name, created__range=[dateStart, dateEnd])
        else:
            receipts_list = Receipt.objects.filter(created__range=[dateStart, dateEnd])

        context['receipts_list'] = receipts_list
        if not receipts_list.exists():
            context['receipts_none'] = True
    else:
        filters = {}
        if dateStart and dateEnd:
            filters['timestamp__range'] = [dateStart, dateEnd]
        if user_name:
            filters['user__username'] = user_name
        if action:
            filters['action_type'] = types_dict.get(action)

        action_history = ActionHistory.objects.filter(**filters).order_by("-timestamp")[:500]
        context['action_list'] = action_history
        if description:
            context['action_list'] = action_history.filter(description__icontains=description).order_by("-timestamp")[:500]

    return render(request, 'shop/action_history.html', context)



def set_sell_price(request):
    context = {}

    if not request.user.is_authenticated:
        messages.error(request, 'Вы не аутентефицированы')
        context['base_page'] = True
        return render(request, 'shop/base_page.html', context)

    user_groups = request.user.groups.all()
    group_names = [group.name for group in user_groups]
    if 'adminGroup' not in group_names and not request.user.is_superuser:
        context['base_page'] = True
        messages.error(request, 'У вас не достаточно прав')
        return render(request, 'shop/base_page.html', context)

    context['set_sell_price'] = True

    cats = list(Category.objects.values_list('name', flat=True))
    context['cats'] = cats

    if request.method == 'POST':
        category = request.POST.get('category')
        percent = request.POST.get('percent')

        if category and percent:

            products = Product.objects.filter(category__name=category)
            cat = Category.objects.get(name=category)

        
            for product in products:
                product.price_sale = product.price_purchase + (product.price_purchase * (Decimal(percent) / 100))
                product.save()
                        

            # Запись в журнал действий
            ActionHistory.objects.create(
                user=request.user,
                action_type='SET_SELL_PRICE',
                category=cat,
                description=f'Установка цены продаж на {str(100+int(percent))}% от цены покупки для категории {category}'
                )

            
            messages.success(request, f'Установка цены продаж на {str(100+int(percent))}% от цены покупки для категории {category}')

        else:

            messages.error(request, f'Заполните все поля')
 
    return render(request, 'shop/set_sell_price.html', context)


def print_qr_images(request):
    context = {}

    if not request.user.is_authenticated:
        messages.error(request, 'Вы не аутентефицированы')
        context['base_page'] = True
        return render(request, 'shop/base_page.html', context)

    user_groups = request.user.groups.all()
    group_names = [group.name for group in user_groups]

    context['print_qr_images'] = True
    
    if request.method == 'POST':
        name = request.POST.get('name')
        products = Product.objects.filter(name__icontains=name)
        context['products'] = products
        context['name'] = name


 
    return render(request, 'shop/print_qr_images.html', context)



def product_detail_for_qr_image(request, product_id):
    # Получаем продукт по ID, если не найден - будет вызвана 404 ошибка
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop/product_detail_for_qr_image.html', {'product': product})



# @login_required
def kassaPage3(request):
    context = {}

    if not request.user.is_authenticated:
        messages.error(request, 'Вы не аутентефицированы')
        context['base_page'] = True
        return render(request, 'shop/base_page.html', context)
    context['kassa_page3'] = True

    return render(request, 'shop/kassaPage3.html', context)


def kurs(request):
    context = {}
    if not request.user.is_authenticated:
        messages.error(request, 'Вы не аутентефицированы')
        context['base_page'] = True
        return render(request, 'shop/base_page.html', context)

    user_groups = request.user.groups.all()
    group_names = [group.name for group in user_groups]
    if 'adminGroup' not in group_names and not request.user.is_superuser:
        context['base_page'] = True
        messages.error(request, 'У вас не достаточно прав')
        return render(request, 'shop/base_page.html', context)

    Kurs.objects.first().kurs
    
    context['kurs'] = True
    context['kurs_digit'] = Kurs.objects.first().kurs


    if request.method == 'POST':
        old_kurs = Kurs.objects.first().kurs
 
        new_kurs = request.POST.get('kurs_digit')
        kurs_digit = new_kurs.replace(',', '.')


        

        kurs_obj = Kurs.objects.first()
        if kurs_obj:
            kurs_obj.kurs = kurs_digit
            kurs_obj.save()
        else:
            Kurs.objects.create(kurs=kurs_digit)

        # Сохраняем информацию в историю действий
        ActionHistory.objects.create(
            user=request.user,
            action_type='SET_KURS',
            description=f'Смена курса с {old_kurs} на {kurs_digit}',
            # Здесь вы можете добавить конкретные поля, если нужно, например, продукт или категория
        )

        context['kurs_digit'] = Kurs.objects.first().kurs

        messages.success(request, f'Смена курса с {old_kurs} на {float(new_kurs)} ')




    return render(request, 'shop/kurs.html', context)



def finded_products_list(request):
    context = {}
    search_word = request.GET.get('search_word')
    context['search_word'] = search_word

    words = search_word.split()  # Разбиваем строку на слова

    # Формируем Q-объект, чтобы искать по всем словам
    q_objects = Q()
    for word in words:
        q_objects &= Q(name__icontains=word)

    products = Product.objects.filter(q_objects)
    context['products'] = products

    print('search_word', search_word)
    return render(request, 'shop/finded_products_list.html', context)





def catalogs(request):
    context = {}
    context['catalogs'] = True

    cats = Category.objects.all()
    context['cats'] = cats

    current_date = datetime.now()
    context['current_date'] = current_date


    if request.method == 'POST':
        cat = request.POST.get('category')
        name = request.POST.get('name')

        context['cat'] = cat
        context['name'] = name

        products = Product.objects.filter(category__name = cat, name__icontains = name)
        context['products'] = products





    # categories = Category.objects.all()
    # catalog_data = {}

    # for category in categories:
    #     products = Product.objects.filter(category=category).order_by("name")
    #     catalog_data[category] = products

    # context['catalog_data'] = catalog_data 

    # current_date = datetime.now()
    # context['current_date'] = current_date

    return render(request, 'shop/catalogs.html', context)










from django.urls import path
from . import views



urlpatterns = [
    path('', views.base_page, name='base_page'),
    path('add-product/', views.add_new_product_and_generate_QRCode, name='add_new_product_and_generate_QRCode'),
    path('Kassa/', views.kassa_page, name='kassa_page'),
    path('Kassa2/', views.kassaPage2, name='kassaPage2'),
    path('Kassa3/', views.kassaPage3, name='kassaPage3'),
    

    # поиск товара после тика
    path('product/<str:product_code_data>/', views.product_detail, name='product_detail'),
    path('get_product_list_from_hand_value/<str:hand_value>/', views.get_product_list_from_hand_value, name='get_product_list_from_hand_value'),
    path('product_detail_with_id/<str:id>/', views.product_detail_with_id, name='product_detail_with_id'),

    # Для проверки совпадений в названии в БД при вводе названия в Input при добавлении продуктв
    path('check-product-name/', views.check_product_name, name='check_product_name'),
 
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('api/product_info_for_buy/', views.product_info_for_buy, name='product_info_for_buy'),
    path('receipts/', views.receipts, name='receipts'),
    path('otchyot/', views.otchyot, name='otchyot'),
    path('stock/', views.stock, name='stock'),
    path('set_discount/', views.set_discount, name='set_discount'),
    path('action_history/', views.action_history, name='action_history'),
    path('set_sell_price/', views.set_sell_price, name='set_sell_price'),
    path('print_qr_images/', views.print_qr_images, name='print_qr_images'),

    path('product_detail_for_qr_image/<int:product_id>/', views.product_detail_for_qr_image, name='product_detail_for_qr_image'),
    path('kurs/', views.kurs, name='kurs'),

    path('finded_products_list/>', views.finded_products_list, name='finded_products_list'),

    path('catalogs/', views.catalogs, name='catalogs'),




    

]



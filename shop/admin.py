from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *




# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display  = ('name', 'price_purchase', 'price_sale', 'profit', 'category', 'get_image')
    

#     def get_image(self, obj):
#         if obj.image:
#             return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" />')
#         return 'Нет изображения'
#     get_image.short_description = 'Фото' 



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ('id','name', 'code_text', 'price_purchase', 'price_sale', 'category', 'cubic_meter')
    # prepopulated_fields = {'slug': ('name',)}
    list_display_links = ('id', 'name')
    list_filter = ('category__name',)
    search_fields = ('name', 'price_purchase', 'price_sale')

    # def get_image(self, obj):
    #     if obj.image:
    #         return mark_safe(f'<img src="{obj.image.url}" width="50" />')
    #     return 'Нет изображения'
    # get_image.short_description = 'Фото продукта'

    # def get_manufacturer_qr_code_image(self, obj):
    #     if obj.manufacturer_qr_code_image:
    #         return mark_safe(f'<img src="{obj.manufacturer_qr_code_image.url}" width="50" />')
    #     return 'Нет изображения'
    # get_manufacturer_qr_code_image.short_description = 'QR производителя' 

    # def get_manufacturer_barcode_image(self, obj):
    #     if obj.manufacturer_barcode_image:
    #         return mark_safe(f'<img src="{obj.manufacturer_barcode_image.url}" width="50" />')
    #     return 'Нет изображения'
    # get_manufacturer_barcode_image.short_description = 'Штрих производителя' 

    # def get_my_generated_qr_code_image(self, obj):
    #     if obj.my_generated_qr_code_image:
    #         return mark_safe(f'<img src="{obj.my_generated_qr_code_image.url}" width="50" />')
    #     return 'Нет изображения'
    # get_my_generated_qr_code_image.short_description = 'QR наш' 

    # def get_my_generated_bar_code_image(self, obj):
    #     if obj.my_generated_bar_code_image:
    #         return mark_safe(f'<img src="{obj.my_generated_bar_code_image.url}" width="50" />')
    #     return 'Нет изображения'
    # get_my_generated_bar_code_image.short_description = 'Штрих наш' 





@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ('name', 'slug')
    prepopulated_fields = {'slug': ('name', )}


@admin.register(Kurs)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ('kurs',)


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display  = ('kassir', 'created')

@admin.register(ReceiptProduct)
class ReceiptProductAdmin(admin.ModelAdmin):
    list_display  = ('receipt', 'product')


@admin.register(ActionHistory)
class ActionHistoryAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'get_action_type_display', 'product', 'receipt', 'category', 'description')
    list_filter = ('action_type', 'user', 'timestamp')  # Фильтры по типу действия, пользователю и времени
    search_fields = ('description', 'user__username', 'action_type')  # Поиск по описанию и имени пользователя
    date_hierarchy = 'timestamp'  # Позволяет сделать иерархический выбор по дате
    
    def get_action_type_display(self, obj):
        return obj.get_action_type_display()
    get_action_type_display.short_description = 'Тип действия'  # Переименовываем заголовок в админке

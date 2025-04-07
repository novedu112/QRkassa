// Установка языка
function setLanguageAddProduct() {
    checkLanguage = localStorage.getItem('selectedLanguage');
    
    let add_new_product_text = document.getElementById('add_new_product_text')
    const productTexts = {
        'RU': 'Добавить новый продукт',
        'TM': 'Täze haryt goşmak',
        'EN': 'Add new product'
    };
    add_new_product_text.innerHTML = productTexts[checkLanguage] || productTexts['TM'];
    
    let add_product_name_text = document.getElementById('add_product_name_text')
    const addProductNameText = {
        'RU': 'Название продукта',
        'TM': 'Harytyn ady',
        'EN': 'Product name'
    };
    add_product_name_text.innerHTML = addProductNameText[checkLanguage] || addProductNameText['TM'];
    
    let add_product_description_text = document.getElementById('add_product_description_text');
    const addProductDescriptionText = {
        'RU': 'Описание продукта',
        'TM': 'Harydyň beýan edilmesi',
        'EN': 'Product description'
    };
    add_product_description_text.innerHTML = addProductDescriptionText[checkLanguage] || addProductDescriptionText['TM'];
    
    let add_product_price_purchase_text = document.getElementById('add_product_price_purchase_text');
    const addProductPricePurchaseText = {
        'RU': 'Цена покупки',
        'TM': 'Satyn alyş bahasy',
        'EN': 'Purchase price'
    };
    add_product_price_purchase_text.innerHTML = addProductPricePurchaseText[checkLanguage] || addProductPricePurchaseText['TM'];
    
    let add_product_price_sale_text = document.getElementById('add_product_price_sale_text');
    const addProductPriceSaleText = {
        'RU': 'Цена продажи',
        'TM': 'Satyş bahasy',
        'EN': 'Sale price'
    };
    add_product_price_sale_text.innerHTML = addProductPriceSaleText[checkLanguage] || addProductPriceSaleText['TM'];

    let add_product_price_sale_optom_text = document.getElementById('add_product_price_sale_optom_text');
    const addProductPriceSaleOptomText = {
        'RU': 'Оптовая цена продажи',
        'TM': 'Wholesale selling price',
        'EN': 'Daşary söwda satuw bahasy'
    };
    add_product_price_sale_optom_text.innerHTML = addProductPriceSaleOptomText[checkLanguage] || addProductPriceSaleOptomText['TM'];
    
    let add_product_discount_text = document.getElementById('add_product_discount_text');
    const addProductDiscountText = {
        'RU': 'Скидка (%)',
        'TM': 'Arzanladyş (%)',
        'EN': 'Discount (%)'
    };
    add_product_discount_text.innerHTML = addProductDiscountText[checkLanguage] || addProductDiscountText['TM'];
    
    let add_product_profit_text = document.getElementById('add_product_profit_text');
    const addProductProfitText = {
        'RU': 'Прибыль (со скидкой не оптом)',
        'TM': 'Girdeji (arzanladyş bilen)',
        'EN': 'Profit (with discount)'
    };
    add_product_profit_text.innerHTML = addProductProfitText[checkLanguage] || addProductProfitText['TM'];
    
    let add_product_stock_text = document.getElementById('add_product_stock_text');
    const addProductStockText = {
        'RU': 'Количество на складе',
        'TM': 'Magazada bolan sany',
        'EN': 'Quantity in stock'
    };
    add_product_stock_text.innerHTML = addProductStockText[checkLanguage] || addProductStockText['TM'];
    
    let add_product_category_text = document.getElementById('add_product_category_text');
    const addProductCategoryText = {
        'RU': 'Категория',
        'TM': 'Kategoriýa',
        'EN': 'Category'
    };
    add_product_category_text.innerHTML = addProductCategoryText[checkLanguage] || addProductCategoryText['TM'];
    
    let add_product_category_disabled_text = document.getElementById('add_product_category_disabled_text');
    const addProductCategoryDisabledText = {
        'RU': 'Выберите категорию',
        'TM': 'Kategoriýany saýlaň',
        'EN': 'Select a category'
    };
    add_product_category_disabled_text.innerHTML = addProductCategoryDisabledText[checkLanguage] || addProductCategoryDisabledText['TM'];
    
    let add_product_image_text = document.getElementById('add_product_image_text');
    const addProductImageText = {
        'RU': 'Фото продукта',
        'TM': 'Harydyň suraty',
        'EN': 'Product photo'
    };
    add_product_image_text.innerHTML = addProductImageText[checkLanguage] || addProductImageText['TM'];
    


    
    let add_product_form_submit_button = document.getElementById('add_product_form_submit_button');
    const addProductFormSubmitButtonText = {
        'RU': 'Сохранить',
        'TM': 'Ýatda saklamak',
        'EN': 'Save'
    };
    add_product_form_submit_button.innerHTML = addProductFormSubmitButtonText[checkLanguage] || addProductFormSubmitButtonText['TM'];
    
    }



const setLanguageKassaPage2 = () => {

    // let nav_kassa2_text = document.getElementById('nav_kassa2_text');
    // const navKassa2Text = {
    //     'RU': 'Касса 2',
    //     'TM': 'Kassa 2',
    //     'EN': 'Cash 2'
    // };
    // nav_kassa2_text.innerHTML = navKassa2Text[checkLanguage] || navKassa2Text['TM'];
    try {
        let th_name = document.getElementById('th_name');
        const thName = {
            'RU': 'Товар',
            'TM': 'Haryt',
            'EN': 'Product'
        };
    th_name.innerHTML = thName[checkLanguage] || thName['TM'];
    } catch {}

    
    try {
    let th_price = document.getElementById('th_price');
    const thPrice = {
        'RU': 'Цена',
        'TM': 'Baha',
        'EN': 'Price'
    };
    th_price.innerHTML = thPrice[checkLanguage] || thPrice['TM'];
    } catch {}

    try {
    let th_count = document.getElementById('th_count');
    const thCount = {
        'RU': 'Количество',
        'TM': 'Sany',
        'EN': 'Count'
    };
    th_count.innerHTML = thCount[checkLanguage] || thCount['TM'];
    } catch {}

    try {
    let th_total_price = document.getElementById('th_total_price');
    const thTotalPrice = {
        'RU': 'Итого',
        'TM': 'Jemi',
        'EN': 'Total'
    };
    th_total_price.innerHTML = thTotalPrice[checkLanguage] || thTotalPrice['TM'];
    } catch {}

    try {
    let th_discount = document.getElementById('th_discount');
    const thDiscount = {
        'RU': 'Скидка',
        'TM': 'Skidka',
        'EN': 'Discount'
    };
    th_discount.innerHTML = thDiscount[checkLanguage] || thDiscount['TM'];
    } catch {}

    try {
        let add_hand_code_btn = document.getElementById('addHandCodeBtn');
        const addHandCodeBtn = {
            'RU': 'Добавить',
            'TM': 'Goşmak',
            'EN': 'Add'
        };
        add_hand_code_btn.innerHTML = addHandCodeBtn[checkLanguage] || addHandCodeBtn['TM'];
    } catch {}

    // receipts
    const receipts_address_text = document.querySelectorAll('.receipts_address_text')
    const ReceiptsAddressText = {
        'RU': 'Magtymguly Şayoly, 7/2',
        'TM': 'Magtymguly Şayoly, 7/2',
        'EN': 'Magtymguly Şayoly, 7/2'
    };    
    receipts_address_text.forEach((element, index) => {
        element.innerHTML = ReceiptsAddressText[checkLanguage] || ReceiptsAddressText['TM'];
    });

    const receipt_shop_name_text = document.querySelectorAll('.receipt_shop_name_text')
    const ReceiptShopNameText = {
        'RU': 'Магазин "VESTEL"',
        'TM': 'Dükan "VESTEL"',
        'EN': 'Store "VESTEL"'
    };    
    receipt_shop_name_text.forEach((element, index) => {
        element.innerHTML = ReceiptShopNameText[checkLanguage] || ReceiptShopNameText['TM'];
    });

    const receipts_store_tel_number_text = document.querySelectorAll('.receipts_store_tel_number_text')
    const ReceiptsStoreTelNumberText = {
        'RU': 'Тел: +993 65 26 56 77, +993 65 09 50 10',
        'TM': 'Tel: +993 65 26 56 77, +993 65 09 50 10',
        'EN': 'Phone: +993 65 26 56 77, +993 65 09 50 10'
    };    
    receipts_store_tel_number_text.forEach((element, index) => {
        element.innerHTML = ReceiptsStoreTelNumberText[checkLanguage] || ReceiptsStoreTelNumberText['TM'];
    });

    const product_text_in_heder_to_receipt_rows = document.querySelectorAll('.product_text_in_heder_to_receipt_rows')
    const ProductTextInHederToReceiptTows = {
        'RU': 'Товар',
        'TM': 'Haryt',
        'EN': 'Product'
    };    
    product_text_in_heder_to_receipt_rows.forEach((element, index) => {
        element.innerHTML = ProductTextInHederToReceiptTows[checkLanguage] || ProductTextInHederToReceiptTows['TM'];
    });

    const count_text_in_heder_to_receipt_rows = document.querySelectorAll('.count_text_in_heder_to_receipt_rows')
    const CountTextInHederToReceiptRows = {
        'RU': 'шт.',
        'TM': 'sany',
        'EN': 'pcs'
    };    
    count_text_in_heder_to_receipt_rows.forEach((element, index) => {
        element.innerHTML = CountTextInHederToReceiptRows[checkLanguage] || CountTextInHederToReceiptRows['TM'];
    });

    const price_to_one_ps_text_in_heder_to_receipt_rows = document.querySelectorAll('.price_to_one_ps_text_in_heder_to_receipt_rows')
    const PriceToOnePsTextInHederToReceiptRows = {
        'RU': 'за 1 шт.',
        'TM': '1san baha',
        'EN': 'per item'
    };    
    price_to_one_ps_text_in_heder_to_receipt_rows.forEach((element, index) => {
        element.innerHTML = PriceToOnePsTextInHederToReceiptRows[checkLanguage] || PriceToOnePsTextInHederToReceiptRows['TM'];
    });

    const total_text_in_heder_to_receipt_rows = document.querySelectorAll('.total_text_in_heder_to_receipt_rows')
    const TotalTextInHederToReceiptRows = {
        'RU': 'Итого',
        'TM': 'Jemi',
        'EN': 'Total'
    };    
    total_text_in_heder_to_receipt_rows.forEach((element, index) => {
        element.innerHTML = TotalTextInHederToReceiptRows[checkLanguage] || TotalTextInHederToReceiptRows['TM'];
    });


    const thank_you_for_your_purchase_text = document.querySelectorAll('.thank_you_for_your_purchase_text')
    const ThankYouForYourPurchaseText = {
        'RU': 'Спасибо за покупку!',
        'TM': 'Satyn alanyňyz üçin sag boluň!',
        'EN': 'Thank you for your purchase!'
    };    
    thank_you_for_your_purchase_text.forEach((element, index) => {
        element.innerHTML = ThankYouForYourPurchaseText[checkLanguage] || ThankYouForYourPurchaseText['TM'];
    });

    const kassir_text = document.querySelectorAll('.kassir_text')
    const KassirText = {
        'RU': 'Кассир: ',
        'TM': 'Kassir: ',
        'EN': 'Cashier: '
    };    
    kassir_text.forEach((element, index) => {
        element.innerHTML = KassirText[checkLanguage] || KassirText['TM'];
    });

    const buy_btn = document.querySelectorAll('.buyBtn')
    const buyBtn = {
        'RU': 'Купить',
        'TM': 'Almak',
        'EN': 'Buy'
    };    
    buy_btn.forEach((element, index) => {
        element.innerHTML = buyBtn[checkLanguage] || buyBtn['TM'];
    });

}


function setLanguageLoginPage () {
    try {
        let login_header_text = document.getElementById('login_header_text')
        const loginHeaderText = {
        'RU': 'Вход в систему',
        'TM': 'Sistema Giriş',
        'EN': 'Login'
        };
        login_header_text.innerHTML = loginHeaderText[checkLanguage] || loginHeaderText['TM'];
    } catch {}
    

    try {
        let login_name_text = document.getElementById('login_name_text')
        const loginNameText = {
        'RU': 'Имя пользователя',
        'TM': 'Ulanyjy ady',
        'EN': 'Username'
        };
        login_name_text.innerHTML = loginNameText[checkLanguage] || loginNameText['TM'];
    } catch {}
  

    try {
        let login_parol_text = document.getElementById('login_parol_text')
        const loginParolText = {
        'RU': 'Пароль',
        'TM': 'Parol',
        'EN': 'Password'
        };
        login_parol_text.innerHTML = loginParolText[checkLanguage] || loginParolText['TM'];
    } catch {}
   

    try {
        let login_in_text = document.getElementById('login_in_text')
        const loginInText = {
        'RU': 'Войти',
        'TM': 'Giriş',
        'EN': 'Login'
        };
        login_in_text.innerHTML = loginInText[checkLanguage] || loginInText['TM'];
    } catch {}
   

   


}

function setLanguageSetDiscountPage () {


}



function setLanguageActionHistoryPage () {
  
    const date_start_text = document.querySelectorAll('.dateStartText')
    const dateStartText = {
        'RU': 'Дата начала',
        'TM': 'Başlangyç senesi',
        'EN': 'Start date'
    };    
    date_start_text.forEach((element, index) => {
        element.innerHTML = dateStartText[checkLanguage] || dateStartText['TM'];
    });

    const date_end_text = document.querySelectorAll('.dateEndText')
    const dateEndText = {
        'RU': 'Дата конца',
        'TM': 'Akhyrky senesi',
        'EN': 'End date'
    };    
    date_end_text.forEach((element, index) => {
        element.innerHTML = dateEndText[checkLanguage] || dateEndText['TM'];
    });
    
}
setLanguageActionHistoryPage();







    
    





  




function setLanguageKassaPage() {
    checkLanguage = localStorage.getItem('selectedLanguage');

    const price_span_text_list = document.querySelectorAll('.price_span_text')
    const PriceSpanTextList = {
        'RU': 'Цена: ',
        'TM': 'Bahasy: ',
        'EN': 'Price: '
    };    
    price_span_text_list.forEach((element, index) => {
        element.innerHTML = PriceSpanTextList[checkLanguage] || PriceSpanTextList['TM'];
    });

    const count_span_text_list = document.querySelectorAll('.count_span_text')
    const CountSpanTextList = {
        'RU': 'Кол-во: ',
        'TM': 'Sany: ',
        'EN': 'Count: '
    };    
    count_span_text_list.forEach((element, index) => {
        element.innerHTML = CountSpanTextList[checkLanguage] || CountSpanTextList['TM'];
    });

    const total_span_text_list = document.querySelectorAll('.total_span_text')
    const TotalSpanTextList = {
        'RU': 'Сумма: ',
        'TM': 'Jemi: ',
        'EN': 'Total: '
    };    
    total_span_text_list.forEach((element, index) => {
        element.innerHTML = TotalSpanTextList[checkLanguage] || TotalSpanTextList['TM'];
    });

    const sale_form_button_text = document.querySelectorAll('.sale_form_button_text')
    const SaleFormButtonText = {
        'RU': 'Продать',
        'TM': 'Satmak',
        'EN': 'Sale'
    };    
    sale_form_button_text.forEach((element, index) => {
        element.innerHTML = SaleFormButtonText[checkLanguage] || SaleFormButtonText['TM'];
    });

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
        'RU': 'Магазин "Пример"',
        'TM': 'Dükan "Misal"',
        'EN': 'Store "Example"'
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
        'RU': 'цена за 1 шт.',
        'TM': '1 sany bahasy',
        'EN': 'price per item'
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




}

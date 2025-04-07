



// После загрузки страницы (фокусить и выделить текст в add name input)
window.onload = function() {
    name.focus();
    name.select();
};


// Калькуляция дохода
function calculateProfit() {
    const price_purchase = parseFloat(pricePurchase.value) || 0;
    const price_sale = parseFloat(priceSale.value) || 0;
    const calc_discount = parseFloat(discount.value) || 0;

    let price_with_discount
    if (calc_discount > 0) {
        // console.log(price_sale, calc_discount, calc_discount/100, price_sale * (calc_discount/100), price_sale - (price_sale * (calc_discount/100)));
        
        price_with_discount = price_sale - (price_sale * (calc_discount/100))
    } else {
        price_with_discount = price_sale
    }
    profit.value = price_with_discount - price_purchase
    if ((price_with_discount - price_purchase) < 0) {
        console.log('ddd');
        
        profit.style.color = 'red';
    } else {
        profit.style.color = 'black';
    }
    
}


// Валидация формы перед отправкой
function validateForm(event) {
    if (parseFloat(profit.value) < 0) {
        event.preventDefault(); // отменить отправку формы
        profit.classList.add('profitIsNegative')
        setTimeout(() => {
            profit.classList.remove('profitIsNegative')
        }, 5000);
        // alert('Ошибка: Вводите только положительные значения.'); // сообщение об ошибке
    }
      
}
productForm.addEventListener('submit', validateForm)



// Закрытие suggets фото
const closeSuggestImage = () => {
    standartImageContainer.classList.remove('d-none');
    suggestImage.classList.add('d-none');
    needDeletePhotoHiddenInput.value = 'yes';
}

// Закрытие миниатюру фото
const closeThumbnailImage = () => {
    standartImageContainer.classList.remove('d-none');
    productImageThumbnail.classList.add('d-none');
    productImgInput.value = ''
    needDeletePhotoHiddenInput.value = 'yes';
}












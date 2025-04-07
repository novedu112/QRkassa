
function deleteProduct(id) {
    const container_id = document.getElementById(`container-id-is-${id}`)

    // const total_price = document.getElementById(`total-price-${id}`)
    const total_umumy_price = document.getElementById('total_umumy_price_id') 
    const calc_total_price = document.getElementById('calc_total_price') 

    const product_price = parseFloat(document.getElementById(`product-price-${id}`).innerText)
    const product_count = parseFloat(document.getElementById(`product-${id}`).innerText)
 
    calc_price = parseFloat(calc_total_price.innerText) - (product_price * product_count)
    calc_total_price.innerText = calc_price
    total_umumy_price.innerText = formatNumber(calc_price)

    container_id.remove()

    const product_id_list = document.querySelectorAll('.product_id_list');
    if (product_id_list.length === 0) {
        const sale_form_button = document.getElementById('sale_form_button')
        sale_form_button.classList.add('d-none')
        total_umumy_price.classList.add('d-none')
    }
}
    

    

    


// Тут добаляется продукт + если на складе нет то карточка красная и исчезает через 5 сек
function addProduct(data) {
    const container = document.getElementById('product_container');
    const total_umumy_price_id = document.getElementById('total_umumy_price_id')
    const total_umumy_price = parseFloat(document.getElementById('total_umumy_price_id').innerHTML)

    const calc_total_tag = document.getElementById('calc_total_price')
    let calc_total_price = parseFloat(document.getElementById('calc_total_price').innerText)
    
    if (data.have_in_stock) {
        if (data.discount > 0) {       
            calc_total_price += total_umumy_price + parseFloat(data.price_with_discount)
            calc_total_tag.innerHTML = calc_total_price
            total_umumy_price_id.innerHTML = formatNumber(calc_total_price)
        } else {
            calc_total_price += parseFloat(data.price_sale)    
            calc_total_tag.innerHTML = calc_total_price
            total_umumy_price_id.innerHTML = formatNumber(calc_total_price)
        }
    }
    
    
    
    
    // Функция для создания карточки
    const createCard = (isOutOfStock) => {
        
        
        
        return  `
        <div class="card kassa_card_container" style="width: 15rem; margin: 5px; ${isOutOfStock ? 'background-color: yellow;' : ''}" id="container-id-is-${data.pk}">
            <div class="product_id_list d-none">${data.pk}</div>
            <div class="d-none">${data.pk}</div>
            <input class="product_id_list" type="hidden" name='product_id_form_input' form='form_for_sale' value="${data.pk}">
            <input class="product_count_list" type="hidden" name='product_count_list' form='form_for_sale' value="1" id="product-count-form-input-${data.pk}">
            <div style="height: 12rem; padding-top: 5px;">
                    <div class="d-flex justify-content-between align-items-center">
                    <button type="button" class="btn-close" aria-label="Close" onclick="deleteProduct(${data.pk})"></button>
                    <span id="count-in-stock-${data.pk}">${data.stock}</span>
                    </div>
                    <hr> 

                <img src="${data.image}" class="card-img-top" alt="...">
            </div>
            <div class="card-body" style="padding: 0 0 10px 0;">
                <h6 class="card-title text-center">${data.name}</h6>
                <div class="border shadow-box">
                    <p class="card-text d-flex justify-content-between border p-2" 
                        ${data.discount 
                            ? 
                            'style="background-color: #eef0fa; margin-bottom: 5px; color:#909090;"' 
                            : 
                            'style="background-color: #cdd6ff; margin-bottom: 5px;"'
                        }>
                            
                        <span class="price_span_text"></span>
                        ${data.discount 
                            ? 
                            `
                            <span class="text-decoration-line-through">${formatNumber(data.price_sale_str)}</span><span></span>
                            <span class="d-none" id="product-price-${data.pk}">${data.price_with_discount}</span>
                            `
                            :
                            `
                            <span class="fw-bold">${formatNumber(data.price_sale_str)}</span><span></span>
                            <span class="d-none" id="product-price-${data.pk}">${data.price_sale}</span>
                            `
                        }
                    </p>
                   ${data.discount
                    ?
                    `<p class="card-text border p-2 d-flex justify-content-between" style="background-color: #cdd6ff; margin-bottom: 5px; align-items:center;">
                        <span><img src="/static/icons/discount1.png" width="30"> ${data.discount}% :</span>
                        <span><span class="fw-bold">${formatNumber(data.price_with_discount)}</span></span>
                    </p>`
                    :
                    ''
                   }
                    <div class="d-flex justify-content-between border p-2" style="align-items: center; background-color: #cdd6ff;">
                        <span style="margin-right: 10px;" class="count_span_text"></span>
                        <span class="fw-bold" id="product-${data.pk}" style="margin-right: 10px;">${data.have_in_stock ? '1' : '0'}</span> 
                        <div class="arrow_button arrow_up" onmousedown="changeCount(${data.pk}, -1)" style="margin-right: 5px;">
                            <div class="arrow"></div>
                        </div>
                        <div class="arrow_button arrow_down" onmousedown="changeCount(${data.pk}, 1)">
                            <div class="arrow"></div>
                        </div>    
                    </div>
                    

                    <div class="d-flex justify-content-between border p-2" style="margin-top: 10px; background-color: #cdd6ff; margin-top: 5px;">
                        <span class="total_span_text"></span>
                        ${data.discount
                            ?
                            `<span class="fw-bold" id="total-price-${data.pk}">${formatNumber(data.price_with_discount)}</span>`
                            :
                            `<span class="fw-bold" id="total-price-${data.pk}">${formatNumber(data.price_sale_str)}</span>`
                        }                           
                    </div>
                </div>
            </div>
        </div>
    `;
    
    }
   
    // Создаем карточку если нет на складе
    const card = createCard(!data.have_in_stock);
    
    // Добавляем карточку в контейнер
    // container.innerHTML += card;
    container.insertAdjacentHTML('afterbegin', card);
    // Удаляем карточку через 5 секунд, если она не в наличии
    if (!data.have_in_stock) {
        setTimeout(() => {
            const cardElement = document.getElementById(`container-id-is-${data.pk}`);
            if (cardElement) {
                cardElement.remove();
            }
        }, 5000);
    } else {
        blink(document.getElementById(`container-id-is-${data.pk}`), 5, 80, 'LightGreen');
    }
    
}
  
// Смена количества и вывод кол-во * цену 
function changeCount(productId, change) {
    const product_count_elem = document.getElementById(`product-${productId}`)
    
    const product_count = parseInt(product_count_elem.innerText)
    const count_in_stock = parseInt(document.getElementById(`count-in-stock-${productId}`).innerText)
    const product_price = parseFloat(document.getElementById(`product-price-${productId}`).innerText)
    const total_price = document.getElementById(`total-price-${productId}`)
    const product_count_form_input = document.getElementById(`product-count-form-input-${productId}`)
    const current_product_container = document.getElementById(`container-id-is-${productId}`);

    
    
    

    if (!(change === 1 && count_in_stock === product_count) && (product_count > 1 || change === 1)) {
        product_count_elem.innerText = product_count + change;
        product_count_form_input.value = product_count + change;
        
        total_price.innerHTML = formatNumber(product_price * (product_count + change));

        const total_umumy_price_id = document.getElementById('total_umumy_price_id')
        // const total_umumy_price = parseFloat(document.getElementById('total_umumy_price_id').innerHTML)
        let calc_total_tag = document.getElementById('calc_total_price')
        let calc_total_price = parseFloat(document.getElementById('calc_total_price').innerText)
        
        
        
        if (change === 1) { 
            calc_total_price += product_price
            calc_total_tag.innerHTML = calc_total_price
            total_umumy_price_id.innerText = formatNumber(calc_total_price)
        } else {
            calc_total_price -= product_price
            calc_total_tag.innerHTML = calc_total_price
            total_umumy_price_id.innerText = formatNumber(calc_total_price)
        }
        
        
        
        blink(document.getElementById(`container-id-is-${productId}`), 8, 50, 'LightGreen');
    } else {
        if (count_in_stock != 0) {
            blink(document.getElementById(`container-id-is-${productId}`), 8, 50, 'LightCoral');
        }
        
    }
}
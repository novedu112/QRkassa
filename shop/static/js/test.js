 `
            <div class="card kassa_card_container" style="width: 15rem; margin: 5px; ${isOutOfStock ? 'background-color: #DA4453;' : ''}" id="container-id-is-${data.pk}">
                <div class="product_id_list d-none">${data.pk}</div>
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
                <div class="card-body" style="padding: 0;">
                    <hr>
                    <h6 class="card-title text-center">${data.name}</h6>
                    <hr>
                    <div class="border shadow-box">
                        <p class="card-text d-flex justify-content-between border p-2" style="background-color: #cdd6ff; margin-bottom: 5px;">
                            <span class="price_span_text"></span>
                            <span class="fw-bold">${data.price_sale_str}</span><span>TMT.</span>
                            <span class="d-none" id="product-price-${data.pk}">${data.price_sale}</span>
                        </p>
                        <div class="d-flex justify-content-between border p-2" style="align-items: center; background-color: #cdd6ff;">
                            <span style="margin-right: 10px;" class="count_span_text"></span>
                            <span class="fw-bold" id="product-${data.pk}" style="margin-right: 10px;">${data.have_in_stock ? '1' : '0'}</span>
                            <div class="arrow_button arrow_up" onclick="changeCount(${data.pk}, -1)" style="margin-right: 5px;">
                                <div class="arrow"></div>
                            </div>
                            <div class="arrow_button arrow_down" onclick="changeCount(${data.pk}, 1)">
                                <div class="arrow"></div>
                            </div>
                        </div>
                        <div class="d-flex justify-content-between border p-2" style="margin-top: 10px; background-color: #cdd6ff; margin-top: 5px;">
                            <span class="total_span_text">Сумма: </span>
                            <span class="fw-bold" id="total-price-${data.pk}">${data.price_sale_str}</span> TMT.
                        </div>
                    </div>
                </div>
                <hr>
            </div>
        `;


         `
            <div class="card kassa_card_container" style="width: 15rem; margin: 5px;" id="container-id-is-${data.pk}">
                <div class="product_id_list d-none">${data.pk}</div>
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
                        <p class="card-text d-flex justify-content-between border p-2" ${data.discount ? 'style="background-color: #eef0fa; margin-bottom: 5px; color:#909090;"' : 'style="background-color: #cdd6ff; margin-bottom: 5px;"'}
                            <span class="price_span_text"></span>
                            ${data.discount 
                                ? 
                                `<span class="text-decoration-line-through">${data.price_with_discount}</span><span></span>`
                                :
                                `<span class="fw-bold">${data.price_sale_str}</span><span></span>`
                            }
                                <span class="d-none" id="product-price-${data.pk}">${data.price_sale}</span>
                        </p>
                       ${data.discount
                        ?
                        `<p class="card-text border p-2 d-flex justify-content-between" style="background-color: #cdd6ff; margin-bottom: 5px; align-items:center;">
                            <span><img src="{% static 'icons/discount1.png' %}" width="30"> 30%:</span>
                            <span><span class="fw-bold">${data.price_with_discount}</span></span>
                        </p>`
                        :
                        pass
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
                                `<span class="fw-bold" id="total-price-${data.pk}">${data.price_with_discount}</span>`
                                :
                                `<span class="fw-bold" id="total-price-${data.pk}">${data.price_sale_str}</span>`
                            }                           
                        </div>
                    </div>
                </div>
            </div>
        `;



        
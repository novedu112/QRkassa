const nav_language_text = document.getElementById('nav_language_text');
const body_themes = document.querySelectorAll('.body-themes');
const languages = document.querySelectorAll('.languages');



body_themes.forEach(item => {
    item.addEventListener('click', function() {
        // Сначала сбрасываем фон для всех элементов
        body_themes.forEach(el => {
            el.style.backgroundColor = ''; // Убираем фон
        });

        // Получаем значение элемента, на который кликнули
        const selectedTheme = this.getAttribute('data-theme');
        console.log('Выбранная тема:', selectedTheme);

        // Удаляем старую тему, если она существует
        localStorage.removeItem('selectedTheme');

        // Сохраняем выбранную тему в localStorage
        localStorage.setItem('selectedTheme', selectedTheme);
        
        const themesClassesList = ['body1', 'body2', 'body3', 'body4', 'body5', 'body6', 'body7', 'body8', 'body9', 'body10'];

        // Удаляем старые классы
        themesClassesList.forEach(themeClass => {
            document.body.classList.remove(themeClass);
        });

        // Добавляем новый класс
        document.body.classList.add(`body${selectedTheme}`);

        // Устанавливаем фон для выбранного элемента
        item.style.backgroundColor = 'rgb(171, 171, 171)';
        setLanguageThemas()
    });
});



    
    languages.forEach(item => {
        item.addEventListener('click', function() {            
            const selectedLanguage = this.getAttribute('data-theme');
            console.log('Выбранный язык:', selectedLanguage);

            // Удаляем старую тему, если она существует
            localStorage.removeItem('selectedLanguage');

            // Сохраняем выбранную тему в localStorage
            localStorage.setItem('selectedLanguage', selectedLanguage);
            // location.reload(); // тут при изменнении языка или темы после покупки совершает повторную покупку
            // window.location.href = 'http://127.0.0.1:8080/shop/Kassa/'; 
            setLanguageKassaPage();
            try {
                setLanguageKassaPage2();
            } catch {}
            
            setLanguageHeader();
            setLanguageThemas();
        });
    });





    

    function setLanguageHeader() {
        checkLanguage = localStorage.getItem('selectedLanguage');

        nav_language_text.innerHTML = checkLanguage || 'TM'

        const nav_add_product_text = document.getElementById('nav_add_product_text')
        const NavProductTexts = {
        'RU': 'Добавить продукт',
        'TM': 'Haryt goşmak',
        'EN': 'Add product'
        };
        nav_add_product_text.innerHTML = NavProductTexts[checkLanguage] || NavProductTexts['TM'];

        const nav_kassa_text = document.getElementById('nav_kassa_text')
        const navKassaText = {
        'RU': 'Касса',
        'TM': 'Kassa',
        'EN': 'Cash'
        };
        nav_kassa_text.innerHTML = navKassaText[checkLanguage] || navKassaText['TM'];

        const nav_main_text = document.getElementById('nav_main_text')
        const navMainText = {
        'RU': 'Главная',
        'TM': 'Esasy',
        'EN': 'Main'
        };
        nav_main_text.innerHTML = navMainText[checkLanguage] || navMainText['TM'];

        let nav_kassa2_text = document.getElementById('nav_kassa2_text');
        const navKassa2Text = {
            'RU': 'Касса 2',
            'TM': 'Kassa 2',
            'EN': 'Cash 2'
        };
        nav_kassa2_text.innerHTML = navKassa2Text[checkLanguage] || navKassa2Text['TM'];

        let nav_login_text = document.getElementById('nav_login_text')
        const navLoginText = {
            'RU': 'Логин',
            'TM': 'Login',
            'EN': 'Login'
        };
        nav_login_text.innerHTML = navLoginText[checkLanguage] || navLoginText['TM'];

        const nav_receipts_text = document.querySelectorAll('.nav_receipts_text')
        const navReceiptsText = {
            'RU': 'Квитанции',
            'TM': 'Kwitansiya',
            'EN': 'Receipts'
        };    
        nav_receipts_text.forEach((element, index) => {
            element.innerHTML = navReceiptsText[checkLanguage] || navReceiptsText['TM'];
        });

        const nav_otchyot_text = document.querySelectorAll('.nav_otchyot_text')
        const navOtchyotText = {
            'RU': 'Отчеты',
            'TM': 'Otchyot',
            'EN': 'Reports'
        };    
        nav_otchyot_text.forEach((element, index) => {
            element.innerHTML = navOtchyotText[checkLanguage] || navOtchyotText['TM'];
        });

        const nav_stock_text = document.querySelectorAll('.nav_stock_text')
        const navStockText = {
            'RU': 'Склад',
            'TM': 'Sklad',
            'EN': 'Stock'
        };    
        nav_stock_text.forEach((element, index) => {
            element.innerHTML = navStockText[checkLanguage] || navStockText['TM'];
        });

        const nav_set_discount_text = document.querySelectorAll('.nav_set_discount_text')
        const navSetDiscountText = {
            'RU': 'Скидка',
            'TM': 'Skidka',
            'EN': 'Discount'
        };    
        nav_set_discount_text.forEach((element, index) => {
            element.innerHTML = navSetDiscountText[checkLanguage] || navSetDiscountText['TM'];
        });

        const nav_action_history_text = document.querySelectorAll('.nav_action_history_text')
        const navActionHistoryPext = {
            'RU': 'История',
            'TM': 'Taryh',
            'EN': 'History'
        };    
        nav_action_history_text.forEach((element, index) => {
            element.innerHTML = navActionHistoryPext[checkLanguage] || navActionHistoryPext['TM'];
        });

        const nav_set_sell_price_text = document.querySelectorAll('.nav_set_sell_price_text')
        const navSetSellPriceText = {
            'RU': 'Цены',
            'TM': 'Baha',
            'EN': 'Price'
        };    
        nav_set_sell_price_text.forEach((element, index) => {
            element.innerHTML = navSetSellPriceText[checkLanguage] || navSetSellPriceText['TM'];
        });
    
        
        

}

    setLanguageHeader();


    function setLanguageThemas(){
        checkLanguage = localStorage.getItem('selectedLanguage');

    let themas1_text = document.getElementById('themas1_text')
    const Themas1Texts = {
    'RU': 'Летний закат',
    'TM': 'Tomus günbatary',
    'EN': 'Summer sunset'
    };
    themas1_text.innerHTML = Themas1Texts[checkLanguage] || Themas1Texts['TM'];

    let themas2_text = document.getElementById('themas2_text')
    const Themas2Texts = {
    'RU': 'Спокойное утро',
    'TM': 'Sakarja irtesi',
    'EN': 'Calm morning'
    };
    themas2_text.innerHTML = Themas2Texts[checkLanguage] || Themas2Texts['TM'];

    let themas3_text = document.getElementById('themas3_text')
    const Themas3Texts = {
    'RU': 'Теплая осень',
    'TM': 'Süýji gökde',
    'EN': 'Warm autumn'
    };
    themas3_text.innerHTML = Themas3Texts[checkLanguage] || Themas3Texts['TM'];


    let themas4_text = document.getElementById('themas4_text')
    const Themas4Texts = {
    'RU': 'Ночной космос',
    'TM': 'Gije älem',
    'EN': 'Night cosmos'
    };
    themas4_text.innerHTML = Themas4Texts[checkLanguage] || Themas4Texts['TM'];

    let themas5_text = document.getElementById('themas5_text')
    const Themas5Texts = {
    'RU': 'Природный зеленый',
    'TM': 'Tejribi ýaşyl',
    'EN': 'Natural green'
    };
    themas5_text.innerHTML = Themas5Texts[checkLanguage] || Themas5Texts['TM'];


    let themas6_text = document.getElementById('themas6_text')
    const Themas6Texts = {
    'RU': 'Пастельный взгляд',
    'TM': 'Pastel garaýyş',
    'EN': 'Pastel view'
    };
    themas6_text.innerHTML = Themas6Texts[checkLanguage] || Themas6Texts['TM'];


    let themas7_text = document.getElementById('themas7_text')
    const Themas7Texts = {
    'RU': 'Энергия вишни',
    'TM': 'Gersin energiýasy',
    'EN': 'Cherry energy'
    };
    themas7_text.innerHTML = Themas7Texts[checkLanguage] || Themas7Texts['TM'];



    let themas8_text = document.getElementById('themas8_text')
    const Themas8Texts = {
    'RU': 'Снежная зима',
    'TM': 'Gardan gyş',
    'EN': 'Snowy winte'
    };
    themas8_text.innerHTML = Themas8Texts[checkLanguage] || Themas8Texts['TM'];


    let themas9_text = document.getElementById('themas9_text')
    const Themas9Texts = {
    'RU': 'Романтика пурпура',
    'TM': 'Purpuryň romantikasy',
    'EN': 'Romance of purple'
    };
    themas9_text.innerHTML = Themas9Texts[checkLanguage] || Themas9Texts['TM'];


    let themas10_text = document.getElementById('themas10_text')
    const Themas10Texts = {
    'RU': 'Морской бриз',
    'TM': 'Dengiz şemaly',
    'EN': 'Sea breeze'
    };
    themas10_text.innerHTML = Themas10Texts[checkLanguage] || Themas10Texts['TM'];
    

}
    
    setLanguageThemas()
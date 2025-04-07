from django import template

register = template.Library()

@register.filter
def format_price(value):
    """ Форматирует цену с пробелами между тысячами """
    return '{:,.2f}'.format(value).replace(',', ' ')


@register.filter
def add_class(field, css_class):
    return field.as_widget(attrs={'class': css_class})


@register.filter
def multiply(quantity, price):
    return quantity * price


@register.filter
def my_format_price(value):
    if value is None:
        return "0,00"
    return f"{value:,.2f}".replace(",", " ").replace(".", ",")


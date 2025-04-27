from django import template

register = template.Library()


@register.filter
def pluralize_russian(value):
    if value == 1:
        return "товар"
    elif value in [2, 3, 4]:
        return "товара"
    else:
        return "товаров"

from django import template

register = template.Library()


@register.filter(name="get_color")
def get_color(colors: list, index: int):
    return colors[index]


@register.filter(name="any_data")
def any_data(data: list):
    return any(data)

from django import template

register = template.Library()


@register.filter(name="get_color")
def get_color(colors: list, index: int):
    return colors[index]

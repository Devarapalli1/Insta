from django import template

register = template.Library()


@register.filter(name="remainder")
def remainder(num, div):
    return num % div

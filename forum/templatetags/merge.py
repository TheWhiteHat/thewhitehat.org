from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(is_safe=False)
@stringfilter
def merge_string(value, arg):
    try:
        return str(value) + str(arg)
    except (TypeError):
        return ''

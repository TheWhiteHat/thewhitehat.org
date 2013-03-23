from django import template
from django.template.defaultfilters import stringfilter
import re

register = template.Library()

class_re = re.compile(r'(?<=class=["\'])(.*)(?=["\'])')

@register.filter(is_safe=False)
@stringfilter
def add_class(value, css_class):
    """Add class to a form"""
    string = unicode(value)
    match = class_re.search(string)
    if match:
        m = re.search(r'^%s$|^%s\s|\s%s\s|\s%s$' % (css_class, css_class,
                                                    css_class, css_class),
                                                    match.group(1))
        print match.group(1)
        if not m:
            return class_re.sub(match.group(1) + " " + css_class, string)
    else:
        return string.replace('>', ' class="%s">' % css_class)
    return value

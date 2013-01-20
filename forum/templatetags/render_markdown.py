from django import template
from markdown import markdown
import re

register = template.Library()

@register.filter()
def render_markdown(value):
    return re.sub(r'\<code\>','<code class="prettyprint">',markdown(str(value)))

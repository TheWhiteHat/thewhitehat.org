import re
from markdown import markdown

def render_markdown(value):
    return re.sub(r'\<code\>','<code class="prettyprint">',markdown(safe_mode='remove',text=str(value)))

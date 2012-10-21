from django.conf.urls.defaults import *
from blog.views import *

urlpatterns=patterns('blog.views',
    url(r'^(?P<slug>\w+)/*$',entry_view,name="entry_view"),
)

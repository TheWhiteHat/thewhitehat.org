from django.conf.urls import patterns, url

urlpatterns = patterns('blog.views',
    url(r'^(?P<slug>\w+)/?$', 'entry_detail', name="entry_detail"),
)

from django.conf.urls import patterns, url

urlpatterns = patterns('blog.views',
    # slug re from django.core.validators.slug_re: [-a-zA-Z0-9_]+
    url(r'^list/?$', 'entry_list', name='entry_list'),
    url(r'^(?P<slug>[-a-zA-Z0-9_]+)/?$', 'entry_detail', name='entry_detail'),
    url(r'^(?:(\d+)/?)?$', 'index', name='blog'),
)

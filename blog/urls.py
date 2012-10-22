from django.conf.urls import patterns, url

urlpatterns = patterns('blog.views',
    # slug re from django.core.validators.slug_re: [-a-zA-Z0-9_]+
    # user re from django.contrib.auth.forms.UserCreatinoForm.username: [\w.@+-]+
    url(r'^author/(?P<author>[\w.@+-]+)/?$', 'entry_list', name='author_entry_list'),
    url(r'^category/(?P<category>[-a-zA-Z0-9_]+)/?$', 'entry_list', name='category_entry_list'),
    url(r'^tag/(?P<tag>[\w.@+-]+)/?$', 'entry_list', name='tag_entry_list'),
    url(r'^archive/?$', 'entry_list', name='entry_list'),
    url(r'^(?P<slug>[-a-zA-Z0-9_]+)/?$', 'entry_detail', name='entry_detail'),
    url(r'^(?:(\d+)/?)?$', 'index', name='blog'),
)

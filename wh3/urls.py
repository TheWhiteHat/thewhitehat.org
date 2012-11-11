from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from django.views.generic import ListView

from blog.models import Entry

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^blog/', include('blog.urls')),
    url(r'^contact/', include('contact.urls')),
    url(r'^$', ListView.as_view(template_name='index.html', context_object_name='entries', queryset=Entry.objects.order_by('-date_created')[:6]), name='index'),
    url(r'^gallery/?', TemplateView.as_view(template_name='single_pages/gallery.html'), name='gallery'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^log', include('whauth.urls')),
)

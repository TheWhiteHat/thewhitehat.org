from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^blog/', include('blog.urls')),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^gallery/?', TemplateView.as_view(template_name='single_pages/gallery.html'), name='gallery'),
    url(r'^admin/', include(admin.site.urls)),

)

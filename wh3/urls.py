from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'wh3.views.home', name='home'),
    # url(r'^wh3/', include('wh3.foo.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

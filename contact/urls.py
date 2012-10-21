from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView

urlpatterns = patterns('contact.views',
    url(r'^$', 'contact', name='contact'),
    url(r'^contact_success/', TemplateView.as_view(template_name='contact/contact_success.html'), name='contact_success'),
)

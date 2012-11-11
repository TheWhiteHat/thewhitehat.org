from django.conf.urls import patterns, url

urlpatterns = patterns('whauth.views',
   url(r'^in/?$','login',name='login'),
   url(r'^out/?$','logouts',name='logout'),
)


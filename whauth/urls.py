from django.conf.urls import patterns, url

urlpatterns = patterns('whauth.views',
   url(r'^login/?$','login',name='login'),
   url(r'^logout/?$','logouts',name='logout'),
   url(r'^register/?$','register',name='register'),
)


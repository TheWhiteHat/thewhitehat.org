from django.conf.urls import patterns, url

urlpatterns = patterns('forum.views',
    url(r'^$','forum_index',name='forum_index'),
    url(r'^questions/(?P<page_number>\d*)$','question_index',name='question_index'),
)

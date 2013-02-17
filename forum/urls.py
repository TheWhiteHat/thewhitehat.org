from django.conf.urls import patterns, url

urlpatterns = patterns('forum.views',
    url(r'^$','forum_index',name='forum_index'),
    url(r'^questions/(?P<page_number>\d*)$','question_index',name='question_index'),
    url(r'^question/(?P<slug>[A-Za-z0-9-]*)$','question_detail',name='question_detail'),
    url(r'^question/vote/$','handle_vote',name='handle_vote'),
    url(r'^question/answer/$','handle_answer',name='handle_answer'),
    url(r'^question/new/$','new_question',name='new_question'),

)

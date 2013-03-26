from django.conf.urls import patterns, url

urlpatterns = patterns('forum.views',
    url(r'^$','forum_index',name='forum_index'),

    # questions urls
    url(r'^questions/(?P<page_number>\d*)$','question_list',name='question_list'),
    url(r'^question/(?P<slug>[A-Za-z0-9-]*)$','question_detail',name='question_detail'),
    url(r'^question/vote/$','handle_vote',name='handle_vote'),
    url(r'^question/answer/$','handle_answer',name='handle_answer'),
    url(r'^question/new/$','new_question',name='new_question'),

    # discussion urls
    url(r'^discussion/(?P<page_number>\d*)$','thread_list',name='thread_list'),
    url(r'^discussion/board/(?P<board_slug>[A-Za-z0-9-]*)/(?P<page_number>\d*)$','thread_list',name='thread_list'),
    url(r'^discussion/thread/(?P<thread_slug>[A-Za-z0-9-]*)/(?P<page_number>\d*)$','thread_detail',name='thread_detail'),
    url(r'^discussion/new/$','new_thread',name='new_thread'),

)

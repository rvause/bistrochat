from django.conf.urls.defaults import *

urlpatterns = patterns('chat.views',
    (r'^$', 'index'),
    (r'^chat/$', 'updateChat'),
    (r'^send/$', 'sendMessage'),
    (r'^users/$', 'updateUserlist'),
    (r'^init/$', 'init'),
)


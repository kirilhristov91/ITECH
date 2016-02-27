from django.conf.urls import patterns, url
from Guess_The_Movie import views

urlpatterns = patterns('',
        url(r'^user/(?P<user_name>[\w\-]+)/$', views.userView, name='user'),
        url(r'^question/(?P<questionID>[\w\-]+)/$', views.guestionView, name='guestionview'),)



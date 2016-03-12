from django.conf.urls import patterns, url
from Guess_The_Movie import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^user/(?P<user_name>[\w\-]+)/$', views.userView, name='user'),
        url(r'^question/(?P<questionID>[\w\-]+)/$', views.guestionView, name='guestionview'),
        url(r'^register/$', views.register, name='register'),
        url(r'^login/$', views.user_login, name='login'),
        url(r'^logout/$', views.user_logout, name='logout'),
         url(r'^game/$', views.game_session, name='login'),
    )


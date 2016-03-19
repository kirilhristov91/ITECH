from django.conf.urls import patterns, url
from Guess_The_Movie import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^user/(?P<user_name>[\w\-]+)/$', views.userView, name='user'),
        url(r'^question/(?P<questionID>[\w\-]+)/$', views.guestionView, name='guestionview'),
        url(r'^register/$', views.register, name='register'),
        url(r'^login/$', views.user_login, name='login'),
        url(r'^logout/$', views.user_logout, name='logout'),
         url(r'^game/$', views.game_session, name='game'),
        url(r'^leaderboard/$', views.leaderboard, name='leaderboard'),
        url(r'^about/$', views.about, name='about'),
        url(r'^question/$', views.question, name='like_category'),
        url(r'^profile/$', views.profile, name='profile'),

        url(r'^question/(?P<question_id>[0-9]+)/update/$', views.update_question, name='update_question'),
        url(r'^summary/(?P<game_session_id>[0-9]+$)',views.summary, name ='sum'),
        url(r'^summary/(?P<movieId>[0-9]+)/update/$',views.add_to_favourites, name='add_to_favourites'),
    )


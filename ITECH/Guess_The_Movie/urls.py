from django.conf.urls import patterns, url
from Guess_The_Movie import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^register/$', views.register, name='register'),
        url(r'^login/$', views.user_login, name='login'),
        url(r'^logout/$', views.user_logout, name='logout'),
        url(r'^game/$', views.game_session, name='game'),
        url(r'^leaderboard/$', views.leaderboard, name='leaderboard'),
        url(r'^about/$', views.about, name='about'),
        url(r'^profile/$', views.profile, name='profile'),
        url(r'^upload_picture/$', views.upload_picture, name='upload_picture'),
        url(r'^question/(?P<question_id>[0-9]+)/update/$', views.update_question, name='update_question'),
        url(r'^summary/(?P<game_session_id>[0-9]+$)',views.summary, name ='sum'),
        url(r'^summary/(?P<movieId>[0-9]+)/update/$',views.add_to_favourites, name='add_to_favourites'),
        url(r'^profile/change_password/$', views.change_password, name='change_password'),
    )


from django.db import models
from django.contrib.auth.models import User

class UserProfile (models.Model):
    user = models.OneToOneField(User)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    game_session_counter = models.IntegerField(default=0)
    total_points = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username


class Movie (models.Model):
    imdb_id = models.CharField(max_length=9)
    title = models.CharField(max_length=256)
    image_url = models.URLField()
    poster_ulr = models.URLField()
    other_options = models.CharField(max_length=1024)


class GameSession (models.Model):
    user = models.ForeignKey(UserProfile)
    timestamp = models.DateTimeField(auto_now_add=True)
    points = models.IntegerField(default=0)


class Question (models.Model):
    game_session = models.ForeignKey(GameSession)
    movie = models.ForeignKey(Movie)
    is_guess_correct = models.BooleanField(default=False)


class Favourites (models.Model):
    user = models.ForeignKey(UserProfile)
    movie = models.ForeignKey(Movie)





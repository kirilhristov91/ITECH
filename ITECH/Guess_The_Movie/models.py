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
    imdb_id = models.CharField(max_length=9,unique=True)
    title = models.CharField(max_length=256)
    image_url = models.URLField()
    poster_url = models.URLField()
    other_options = models.CharField(max_length=1024)

    def __unicode__(self):
        return self.title


class GameSession (models.Model):
    user = models.ForeignKey(UserProfile)
    timestamp = models.DateTimeField(auto_now_add=True)
    points = models.IntegerField(default=0)


class Question (models.Model):
    game_session = models.ForeignKey(GameSession)
    movie = models.ForeignKey(Movie)
    index = models.IntegerField()
    is_guess_correct = models.BooleanField(default=False)


class Answer(models.Model):
    question = models.ForeignKey(Question)
    text = models.CharField(max_length = 256)


class Favourites (models.Model):
    user = models.ForeignKey(UserProfile)
    movie = models.ForeignKey(Movie)






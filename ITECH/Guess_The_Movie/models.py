from django.db import models


class User (models.Model):
    username = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=64)
    email = models.CharField(max_length=128, unique=True)
    game_session_counter = models.IntegerField(default=0)
    total_points = models.IntegerField(default=0)

    def __unicode__(self):
        return self.username


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField()


class GameSession (models.Model):
    user_id = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now_add=True)
    points = models.IntegerField(defaul=0)


class Question (models.Model):
    game_session_id = models.ForeignKey(GameSession)
    option_a = models.CharField(max_lenght=128)
    option_b = models.CharField(max_lenght=128)
    option_c = models.CharField(max_lenght=128)
    option_d = models.CharField(max_lenght=128)
    image = models.URLField()
    correct_answer = models.IntegerField(defaul=0)
    selected = models.IntegerField(defaul=0)




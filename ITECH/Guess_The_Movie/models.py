from django.db import models
from django.contrib.auth.models import User

class UserProfile (models.Model):

    user = models.OneToOneField(User)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    game_session_counter = models.IntegerField(default=0)
    total_points = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username


class GameSession (models.Model):
    user_id = models.ForeignKey(UserProfile)
    timestamp = models.DateTimeField(auto_now_add=True)
    points = models.IntegerField(default=0)


class Question (models.Model):
    game_session_id = models.ForeignKey(GameSession)
    option_a = models.CharField(max_length=256)
    option_b = models.CharField(max_length=256)
    option_c = models.CharField(max_length=256)
    option_d = models.CharField(max_length=256)
    image = models.ImageField(upload_to='question_images', blank=True)
    correct_answer = models.IntegerField(default=0)
    selected = models.IntegerField(default=0)




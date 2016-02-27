from django.contrib import admin
from Guess_The_Movie.models import UserProfile, Question, GameSession


class UserProfileAdmin(admin.ModelAdmin):
   list_display = ('user', 'picture', 'game_session_counter', 'total_points')


class GameSessionAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'timestamp', 'points')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('game_session_id', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer', 'selected')

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(GameSession, GameSessionAdmin)
admin.site.register(Question, QuestionAdmin)

from django.contrib import admin
from Guess_The_Movie.models import UserProfile, Question, GameSession, Movie, Favourites, Answer


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'picture', 'game_session_counter', 'total_points')


class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','image_url')


class GameSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'points')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id','game_session', 'movie', 'is_guess_correct')


class FavouritesAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie')


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text', 'question')

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(GameSession, GameSessionAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Favourites, FavouritesAdmin)
admin.site.register(Answer, AnswerAdmin)
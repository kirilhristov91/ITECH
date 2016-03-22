from django import forms
from django.contrib.auth.models import User
from guess_the_movie.models import UserProfile

class UserForm(forms.ModelForm):
   # username = forms.CharField(max_length = 128, help_text = "Please enter username.")
    #password = forms.CharField(max_length = 64, widget = forms.PasswordField, help_text = "Please enter your password.")
    #email = forms.EmailField(max_length =  128)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)


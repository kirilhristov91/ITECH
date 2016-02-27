from django import forms
from Guess_The_Movie.models import UserProfile

class UserForm(forms.ModelForm):
    password = forms.CharField(max_length = 64, widget = forms.PasswordField, help_text = "Please enter your password.")


    class Meta:
        model = UserProfile
        fileds = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fileds = ('picture')

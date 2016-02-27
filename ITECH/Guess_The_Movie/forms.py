from django import forms
from rango.models import User

class UserForm(forms.ModelForm):

    username = forms.CharField(max_length = 128, help_text = "Please enter username.")
    password = forms.CharField(max_length = 64, widget = forms.PasswordField, help_text = "Please enter your password.")
    email = forms.EmailField(max_length =  128)

    class Meta:
        model = User

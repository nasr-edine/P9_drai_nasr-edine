from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username',)  # new


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username',)  # new

# creating a form


class FollowerForm(forms.Form):
    follower = forms.CharField(max_length=200, label="Nom de l'utilisateur a suivre", widget=forms.TextInput(
        attrs={'placeholder': "Nom d'utilisateur"}))
    title = forms.CharField(max_length=200, label='Titre', widget=forms.TextInput(
        attrs={'placeholder': 'Titre du ticket'}))

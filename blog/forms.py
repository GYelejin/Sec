from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from django.forms import ModelForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 
        'password1', 'password2']
        labels = {
            'username':'Логин', 
            'password1':'Пароль', 
            'password2': 'Подтверждение пароля'

        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'about']
        labels = {
            'username': 'Псевдоним',
            'about': 'Подробнее о себе'
            }
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)


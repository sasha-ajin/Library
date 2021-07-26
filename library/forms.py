from django.forms import Form, CharField, PasswordInput, DateTimeField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . import models


class LoginUserForm(Form):
    username = CharField(label='Username...', max_length=100, help_text='Username...')
    password = CharField(label='Password...', widget=PasswordInput(), help_text='Password...')


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class DateTimeForm(Form):
    time = DateTimeField(required=True,  input_formats=['%Y-%m-%d %H:%M'],
                         initial=None, disabled=False)

# help_text=f"{models.Time.objects.get(id=1)} time now"

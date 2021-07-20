from django.forms import Form, CharField, PasswordInput, DateTimeField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LoginUserForm(Form):
    username = CharField(label='Username...', max_length=100, help_text='Username...')
    password = CharField(label='Password...', widget=PasswordInput(), help_text='Password...')


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class DateTimeForm(Form):
    time = DateTimeField(help_text='2021-06-30 08:11:01', input_formats=['%Y-%m-%d %H:%M:%S'])

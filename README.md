# Running localy 

### Cloning

```
git clone https://github.com/sasha-ajin/django-library.git
```

### Installing requirements

Before you do that, you should have installed python on your machine

```
python3 -m venv ~/.../environment

cd  ~/.../environment

source bin/activate

pip install django 

pip install django djangorestframework

pip install Pillows
```

### Connect DataBase

In **library/settings.py** . More about connecting db here https://docs.djangoproject.com/en/4.0/ref/databases/

```
...
DATABASES = {
    'default': {
        'ENGINE': '',
        'NAME': '...',
        'HOST': '...',
        'PORT': '...',
        'USER': '...',
        'PASSWORD': '...',
    }
}
...
```
After that,you shoud install your engine to environment, if it is MySQL, it will be 

```
pip install mysqlclient
pip install sqlparse
```

And now write in console

```
python manage.py migrate
```
### Create super-user to go in django-admin-panel

```
python manage.py createsuperuser

Username: admin
Email address: admin@admin.com
Password:
Password (again):

Superuser created successfully.

```

### Running

```
python manage.py runserver 
```
And now go to http://127.0.0.1:8000/



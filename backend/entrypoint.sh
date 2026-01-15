#!/bin/sh
# cd ./project
python manage.py makemigrations
python manage.py migrate

# Создать суперпользователя, если он не существует
python manage.py shell <<'PY'
import os
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, password=password)
PY

python manage.py runserver 0.0.0.0:8000

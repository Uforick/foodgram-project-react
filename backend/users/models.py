from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import CharField


class CustomUser(AbstractUser):
    username = CharField(max_length=30, unique=True)
    email = models.EmailField(('email address'), unique=True)
    first_name = models.CharField(max_length=30, null=False, blank=False)
    last_name = models.CharField(max_length=30, null=False, blank=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'password',
        'first_name',
        'last_name'
    ]

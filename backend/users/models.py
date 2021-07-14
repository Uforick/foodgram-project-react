from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(
        self,
        email,
        username,
        password,
        first_name,
        last_name,
    ):
        user = self.model(
            email=email,
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.is_superuser = False
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email,
        username,
        password,
        first_name,
        last_name,
    ):
        user = self.model(
            email=email,
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    email = models.EmailField
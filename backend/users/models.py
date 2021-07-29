from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    first_name = models.CharField(
        'first name',
        max_length=30,
        blank=False,
    )
    last_name = models.CharField(
        'last name',
        max_length=150,
        blank=False,
    )
    email = models.EmailField(
        'email address',
        blank=False,
        unique=True,
    )

    class Meta:
        app_label = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class FollowModel(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='subscribed_on',
        help_text='Кто подписывается'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='subscriber',
        help_text='На кого подписываются'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='subscribe')
        ]

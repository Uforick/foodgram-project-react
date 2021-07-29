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

    def __str__(self):
        return self.username


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

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class Ingredients(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Название'))
    quantity = models.IntegerField(max_length=10, verbose_name=_('Количество'))
    measure = models.CharField(max_length=10, verbose_name=_('Мера измерения'))

    class Meta:
        verbose_name = _('Ингредиент')
        verbose_name_plural = _('Ингредиенты')
        ordering = ('id',)

    def __str__(self):
        return self.name

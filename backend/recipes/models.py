from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class TagModel(models.Model):
    name = models.CharField(
        max_length=15,
        blank=False,
        null=False,
        unique=True,
        verbose_name='Текст тега'
    )
    color = models.CharField(
        max_length=7,
        blank=False,
        null=False,
        unique=True,
        verbose_name='Цвет тега'
    )
    slug = models.SlugField(
        max_length=30,
        unique=True,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        return self.name


class IngredientModel(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        unique=True
    )
    # quantity = models.IntegerField(
    #     max_length=10,
    #     verbose_name='Количество',
    #     null=True,
    #     blank=True
    # )
    measurement_unit = models.CharField(
        max_length=10,
        verbose_name='Мера измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return self.name


class RecipeModel(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        unique=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=1,
        related_name='recipes',
        verbose_name='Автор',
    )
    image = models.ImageField(
        upload_to='static/recipes/',
        blank=True,
        null=True,
        verbose_name='Картинка',
    )
    text = models.TextField(
        blank=False,
        verbose_name='Рецепт',
    )
    ingredients = models.ManyToManyField(
        IngredientModel,
        related_name='recipes',
        verbose_name='Ингредиенты',
    )
    tags = models.ManyToManyField(
        TagModel,
        related_name='recipes',
        verbose_name='Теги',
    )
    cooking_time = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Время приготовления',
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-id',)

    def __str__(self):
        return self.name

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.deletion import SET_NULL


User = get_user_model()


class TagModel(models.Model):
    tags_text = models.CharField(
        max_length=15,
        blank=False,
        null=False,
        unique=True,
        verbose_name='Текст тега'
    )
    color_HEX = models.CharField(
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
        ordering = ('tags_text',)

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
    measure = models.CharField(
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
        on_delete=models.SET_NULL,
        related_name='recipes',
        verbose_name='Автор',
    )
    picture = models.ImageField(
        upload_to='recipes/',
        blank=False,
        null=False,
        verbose_name='Картинка',
    )
    recipes_text = models.TextField(
        blank=False,
        verbose_name='Рецепт',
    )
    recipes_ingredients = models.ManyToManyField(
        IngredientModel,
        on_delete=models.SET_NULL,
        related_name='recipes',
        verbose_name='Ингредиенты',
    )
    recipes_tag = models.ManyToManyField(
        TagModel,
        on_delete=SET_NULL,
        related_name='recipes',
        verbose_name='Теги',
    )
    cooking_time = models.PositiveSmallIntegerField(
        default=1,
        max_length=4,
        verbose_name='Время приготовления',
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-id',)

    def __str__(self):
        return self.name

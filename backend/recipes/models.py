from django.db import models
from users.models import CustomUser as User


class TagModel(models.Model):
    name = models.CharField(
        max_length=15,
        blank=False,
        null=False,
        unique=True,
        verbose_name='Текст тега',
    )
    color = models.CharField(
        max_length=7,
        default='ff0000',
        verbose_name='Цвет тега',
    )
    slug = models.SlugField(
        max_length=30,
        unique=True,
        verbose_name='Имя адреса тега',
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
        unique=True,
    )
    measurement_unit = models.CharField(
        max_length=10,
        verbose_name='Мера измерения',
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
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name


class AddIngredientInRecModel(models.Model):
    ingredient = models.ForeignKey(
        IngredientModel,
        on_delete=models.CASCADE,
        verbose_name='Ингридиент для рецепта',
    )
    recipe = models.ForeignKey(
        RecipeModel,
        on_delete=models.CASCADE,
        verbose_name='Сам рецепт',
    )
    add_quantity = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Добавить количество ингредиента',
    )

    class Meta:
        verbose_name = 'Количество или масса ингредиента'

    def __str__(self):
        return f'{self.ingredient} {self.recipe}'


class ShoppingListModel(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='purchases',
        verbose_name='Покупатель',
    )
    recipe = models.ForeignKey(
        RecipeModel,
        on_delete=models.CASCADE,
        related_name='customers',
        verbose_name='Рецепт для покупки',
    )
    add_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
    )

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        ordering = ('-add_date',)


class FavoriteRecipeModel(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='who_add_in_favorite',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        RecipeModel,
        on_delete=models.CASCADE,
        related_name='recipe_in_favorite',
        verbose_name='Рецепт',
    )
    add_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        ordering = ('-add_date',)

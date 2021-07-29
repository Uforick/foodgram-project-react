from django.db import models

from users.models import CustomUser as User


class TagModel(models.Model):
    name = models.CharField(
        max_length=15,
        blank=False,
        null=False,
        unique=True,
        verbose_name='Тег',
    )
    color = models.CharField(
        max_length=7,
        default='#ff0000',
        verbose_name='Цвет',
    )
    slug = models.SlugField(
        max_length=30,
        unique=True,
        verbose_name='Адрес',
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
        related_name='recipes',
        verbose_name='Автор',
    )
    image = models.ImageField(
        upload_to='static/recipes/',
        blank=False,
        verbose_name='Картинка',
    )
    text = models.TextField(
        blank=False,
        verbose_name='Рецепт',
    )
    ingredients = models.ManyToManyField(
        IngredientModel,
        related_name='recipes',
        through='AddIngredientInRecModel',
        blank=False,
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

    def __str__(self):
        return self.name


class AddIngredientInRecModel(models.Model):
    ingredient = models.ForeignKey(
        IngredientModel,
        on_delete=models.CASCADE,
        related_name='amounts',
        verbose_name='Ингридиент для рецепта',
    )
    recipe = models.ForeignKey(
        RecipeModel,
        on_delete=models.CASCADE,
        related_name='amounts',
        verbose_name='Сам рецепт',
    )
    amount = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Количество или масса ингредиента'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='recipe_ingredient_unique'
            )
        ]

    def __str__(self):
        return f'{self.ingredient} {self.recipe}'


class ShoppingListModel(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='is_in_shopping_cart',
        verbose_name='Покупатель',
    )
    recipe = models.ForeignKey(
        RecipeModel,
        on_delete=models.CASCADE,
        related_name='is_in_shopping_cart',
        verbose_name='Рецепт для покупки',
    )

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='cart_user_recept_unique'
            )
        ]

    def __str__(self):
        return f'{self.recipe} {self.user}'


class FavoriteRecipeModel(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='is_favorited',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        RecipeModel,
        on_delete=models.CASCADE,
        related_name='is_favorited',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='user_recept_unique'
            )
        ]

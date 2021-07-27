# Generated by Django 3.2.5 on 2021-07-27 12:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('recipes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppinglistmodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopper', to=settings.AUTH_USER_MODEL, verbose_name='Покупатель'),
        ),
        migrations.AddField(
            model_name='recipemodel',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AddField(
            model_name='recipemodel',
            name='ingredients',
            field=models.ManyToManyField(related_name='recipes', to='recipes.IngredientModel', verbose_name='Ингредиенты'),
        ),
        migrations.AddField(
            model_name='recipemodel',
            name='tags',
            field=models.ManyToManyField(related_name='recipes', to='recipes.TagModel', verbose_name='Теги'),
        ),
        migrations.AddField(
            model_name='favoriterecipemodel',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_in_favorite', to='recipes.recipemodel', verbose_name='Рецепт'),
        ),
        migrations.AddField(
            model_name='favoriterecipemodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='who_add_in_favorite', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='addingredientinrecmodel',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.ingredientmodel', verbose_name='Ингридиент для рецепта'),
        ),
        migrations.AddField(
            model_name='addingredientinrecmodel',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipemodel', verbose_name='Сам рецепт'),
        ),
    ]

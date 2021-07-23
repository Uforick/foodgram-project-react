# Generated by Django 3.2.5 on 2021-07-23 15:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0002_auto_20210722_0856'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipemodel',
            options={'ordering': ('-pub_date',), 'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.AddField(
            model_name='recipemodel',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата публикации'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tagmodel',
            name='color',
            field=models.CharField(default='ff0000', max_length=7, verbose_name='Цвет тега'),
        ),
        migrations.AlterField(
            model_name='tagmodel',
            name='slug',
            field=models.SlugField(max_length=30, unique=True, verbose_name='Имя адреса тега'),
        ),
        migrations.CreateModel(
            name='ShoppingListModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customers', to='recipes.recipemodel', verbose_name='Рецепт для покупки')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopper', to=settings.AUTH_USER_MODEL, verbose_name='Покупатель')),
            ],
            options={
                'verbose_name': 'Покупка',
                'verbose_name_plural': 'Покупки',
                'ordering': ('-add_date',),
            },
        ),
        migrations.CreateModel(
            name='FavoriteRecipeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_in_favorite', to='recipes.recipemodel', verbose_name='Рецепт')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='who_add_in_favorite', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Избранное',
                'verbose_name_plural': 'Избранное',
                'ordering': ('-add_date',),
            },
        ),
        migrations.CreateModel(
            name='AddIngredientInRecModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_quantity', models.PositiveSmallIntegerField(default=1, verbose_name='Добавить количество ингредиента')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.ingredientmodel', verbose_name='Ингридиент для рецепта')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipemodel', verbose_name='Сам рецепт')),
            ],
            options={
                'verbose_name': 'Количество или масса ингредиента',
            },
        ),
    ]
from django.contrib import admin

from .models import RecipeModel, TagModel, IngredientModel


class RecipeAdmin(admin.ModelAdmin):

    list_display = (
        # 'id',
        # 'tags',
        'author',
        # 'ingredients',
        # 'is_favorited',
        # 'is_in_shopping_cart',
        'name',
        # 'image',
        # 'text',
        # 'cooking_time',
    )
    list_filter = ('name',)
    empty_value_display = 'пусто'


class TagAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        # 'color',
        # 'slug',
    )
    list_display = ('name',)
    empty_value_display = 'пусто'


class IngredientAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        # 'measurement_unit',
    )
    list_display = ('name',)
    empty_value_display = 'пусто'


admin.site.register(RecipeModel, RecipeAdmin)
admin.site.register(TagModel, TagAdmin)
admin.site.register(IngredientModel, IngredientAdmin)

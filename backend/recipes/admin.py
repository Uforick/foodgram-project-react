from django.contrib import admin
from django.utils.html import format_html

from .models import (AddIngredientInRecModel, IngredientModel, RecipeModel,
                     TagModel)


@admin.register(TagModel)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')
    search_fields = ('name', 'slug')
    empty_value_display = '-пусто-'
    list_filter = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


class RecipeIngredientInLine(admin.TabularInline):
    model = AddIngredientInRecModel


@admin.register(IngredientModel)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(RecipeModel)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'image_tag')
    search_fields = ('user', 'author')
    list_filter = ('author', 'name', 'tags')
    inlines = [RecipeIngredientInLine]
    readonly_fields = ('image_tag',)

    def image_tag(self, instance):
        return format_html(
            '<img src="{0}" style="max-width: 40%"/>',
            instance.image.url
        )

    image_tag.short_description = 'Предпросмотр изображения'

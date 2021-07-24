from django.contrib import admin

from .models import (
    FavoriteRecipeModel,
    IngredientModel,
    RecipeModel,
    ShoppingListModel,
    TagModel
)


class RecipeAdmin(admin.ModelAdmin):
    list_filter = ('author', 'name', 'tags')
    list_display = ('name', 'followers')

    @admin.display(empty_value=None)
    def followers(self, obj):
        return obj.favorite_recipe.all().count()


class IngredientAdmin(admin.ModelAdmin):
    list_filter = ('name', )


admin.site.register(TagModel)
admin.site.register(IngredientModel, IngredientAdmin)
admin.site.register(RecipeModel, RecipeAdmin)
admin.site.register(FavoriteRecipeModel)
admin.site.register(ShoppingListModel)

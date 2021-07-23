import django_filters as filters

from .models import RecipeModel


class RecipeFilter(filters.FilterSet):
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug'
    )
    is_favorited = filters.BooleanFilter(method='get_favorite')
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart'
    )

    class Meta:
        model = RecipeModel
        fields = ('is_favorited', 'is_in_shopping_cart', 'author', 'tags')

    def get_favorite(self, queryset, name, value):
        user = self.request.user
        if value:
            return RecipeModel.objects.filter(favorite_recipe__user=user)
        return RecipeModel.objects.all()

    def get_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value:
            return RecipeModel.objects.filter(customers__user=user)
        return RecipeModel.objects.all()

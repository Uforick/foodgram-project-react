from django_filters import CharFilter, FilterSet
from django_filters.filters import BooleanFilter

from .models import Ingredient, Recipe


class RecipeFilter(FilterSet):
    tags = CharFilter(field_name='tags__slug', method='filter_tags')
    is_favorited = BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = BooleanFilter(method='filter_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ('is_favorited', 'is_in_shopping_cart', 'author', 'tags')

    def filter_tags(self, queryset, slug, tags):
        tags = self.request.query_params.getlist('tags')
        return queryset.filter(
            tags__slug__in=tags
        ).distinct()

    def filter_is_favorited(self, queryset, is_favorited, slug):
        user = self.request.user
        if not user.is_authenticated:
            return queryset
        bool_dict = {'true': True, 'false': False}
        is_favorited = self.request.query_params.get('is_favorited', False)
        if bool_dict.get(is_favorited, False):
            return queryset.filter(
                is_favorited__user=self.request.user
            ).distinct()
        return queryset

    def filter_is_in_shopping_cart(self, queryset, is_in_shopping_cart, slug):
        user = self.request.user
        if not user.is_authenticated:
            return queryset
        bool_dict = {'true': True, 'false': False}
        is_favorited = self.request.query_params.get(
            'is_in_shopping_cart',
            False,
        )
        if bool_dict.get(is_favorited, False):
            return queryset.filter(
                is_in_shopping_cart__user=self.request.user
            ).distinct()
        return queryset


class IngredientNameFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='name__icontains')

    class Meta:
        model = Ingredient
        fields = ('name',)

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CalcPrintShopListView, FavouriteViewSet, IngredientViewSet,
                    RecipeViewSet, ShoppingListViewSet, TagViewSet)

router = DefaultRouter()

router.register(
    r'recipes',
    RecipeViewSet,
    basename='recipes',
)
router.register(
    r'tags',
    TagViewSet,
    basename='tags',
)
router.register(
    r'ingredients',
    IngredientViewSet,
    basename='ingredients',
)

urlpatterns = [
    path(
        'recipes/<int:recipe_id>/favorite/',
        FavouriteViewSet.as_view(),
        name='add_recipe_favorite'
    ),
    path(
        'recipes/<int:recipe_id>/shopping_cart/',
        ShoppingListViewSet.as_view(),
        name='add_recipe_shop'
    ),
    path(
        'recipes/download_shopping_cart/',
        CalcPrintShopListView.as_view(),
        name='shop_list'
    ),
    path('', include(router.urls)),
]

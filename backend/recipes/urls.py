from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    RecipeViewSet,
    TagViewSet,
    IngredientViewSet
)

router = DefaultRouter()

router.register(
    r'recipes/',
    RecipeViewSet,
    basename='recipes',
)
router.register(
    r'tags/',
    TagViewSet,
    basename='tags',
)
router.register(
    r'ingredients/',
    IngredientViewSet,
    basename='ingredients',
)

urlpatterns = [
    path('', include(router.urls)),
]

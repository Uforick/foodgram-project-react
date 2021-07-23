from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import permission_classes
from rest_framework import filters, status, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import (
    RecipeModel,
    TagModel,
    IngredientModel,
    FavoriteRecipeModel,
    ShoppingListModel,
    AddIngredientInRecModel,
)
from . import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = RecipeModel.objects.all()
    serializer_class = serializers.RecipeSerializer
    http_method_names = ('get', 'post', 'put', 'delete')

    @permission_classes([IsAuthenticated])
    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    queryset = TagModel.objects.all()
    serializer_class = serializers.TagSerializer
    http_method_names = ('get',)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = IngredientModel.objects.all()
    permission_classes = AllowAny
    serializer_class = serializers.IngredientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    http_method_names = ('get',)


class FavouriteViewSet(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(RecipeModel, id=recipe_id)
        if FavoriteRecipeModel.objects.filter(
            user=user,
            recipe=recipe
        ).exists():
            return Response(
                'Вы уже добавили рецепт в избранное',
                status=status.HTTP_400_BAD_REQUEST,
            )
        FavoriteRecipeModel.objects.create(user=user, recipe=recipe)
        serializer = serializers.FavoriteRecipeSerializer(recipe)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def delete(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(RecipeModel, id=recipe_id)
        favorite_obj = get_object_or_404(
            FavoriteRecipeModel,
            user=user,
            recipe=recipe,
        )
        if not favorite_obj:
            return Response(
                'Рецепт не был в избранном',
                status=status.HTTP_400_BAD_REQUEST,
            )
        favorite_obj.delete()
        return Response(
            'Удалено',
            status=status.HTTP_204_NO_CONTENT,
        )


class ShoppingListViewSet(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(RecipeModel, id=recipe_id)
        if ShoppingListModel.objects.filter(user=user, recipe=recipe).exists():
            return Response(
                'Вы уже добавили рецепт в список покупок',
                status=status.HTTP_400_BAD_REQUEST,
            )
        ShoppingListModel.objects.create(user=user, recipe=recipe)
        serializer = serializers.FavoriteRecipeSerializer(recipe)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def delete(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(RecipeModel, id=recipe_id)
        shopping_list_obj = get_object_or_404(
            ShoppingListModel, user=user, recipe=recipe)
        if not shopping_list_obj:
            return Response(
                'Рецепт не был в списке покупок',
                status=status.HTTP_400_BAD_REQUEST,
            )
        shopping_list_obj.delete()
        return Response(
            'Удалено',
            status=status.HTTP_204_NO_CONTENT,
        )


class CalcPrintShopListView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user = request.user
        shopping_cart = user.shopper.all()
        buying_list = {}
        for record in shopping_cart:
            recipe = record.recipe
            ingredients = AddIngredientInRecModel.objects.filter(recipe=recipe)
            for ingredient in ingredients:
                add_quantity = ingredient.add_quantity
                name = ingredient.ingredient.name
                measurement_unit = ingredient.ingredient.measurement_unit
                if name not in buying_list:
                    buying_list[name] = {
                        'measurement_unit': measurement_unit,
                        'add_quantity': add_quantity
                    }
                else:
                    buying_list[name]['add_quantity'] = (
                        buying_list[name]['add_quantity'] + add_quantity
                    )

        ingredient_list = []
        for item in buying_list:
            ingredient_list.append(f'{item} - {buying_list[item]["add_quantity"]} '
                                   f'{buying_list[item]["measurement_unit"]} \n')
        # ingredient_list.append('\n')
        response = HttpResponse(ingredient_list, 'Content-Type: text/plain')
        response['Content-Disposition'] = 'attachment; filename="ingredient_list.txt"'
        return response

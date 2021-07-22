from rest_framework import serializers

from .models import (
    RecipeModel,
    TagModel,
    IngredientModel,
    AddIngredientInRecModel,
    FavoriteRecipeModel
)


class RecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecipeModel
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = TagModel
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = IngredientModel
        fields = '__all__'


class AddIngredientInRecSerializer(serializers.ModelSerializer):

    class Meta:
        model = AddIngredientInRecModel
        fields = '__all__'


class FavoriteRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = FavoriteRecipeModel
        fields = '__all__'


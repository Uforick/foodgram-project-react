from rest_framework import serializers

from .models import RecipeModel, TagModel, IngredientModel


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

import base64
import imghdr
import uuid

import six
from rest_framework import serializers
from rest_framework.fields import ImageField
from django.core.files.base import ContentFile

from users.models import FollowModel
from users.serializers import UserSerializerModified

from .models import (AddIngredientInRecModel, FavoriteRecipeModel,
                     IngredientModel, RecipeModel, ShoppingListModel, TagModel,
                     User)


class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')
            file_name = str(uuid.uuid4())[:12]
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = '%s.%s' % (file_name, file_extension, )
            data = ContentFile(decoded_file, name=complete_file_name)
        return super().to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        extension = imghdr.what(file_name, decoded_file)
        if extension == 'jpeg':
            extension = 'jpg'
        return extension


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = TagModel
        fields = ('id', 'name', 'color', 'slug')


class IngredientReadSerializer(serializers.ModelSerializer):

    class Meta():
        model = IngredientModel
        fields = ('id', 'name', 'measurement_unit')
        read_only_fields = ('id', 'name', 'measurement_unit')


class IngredientWriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta():
        model = IngredientModel
        fields = ('id', 'amount')


class FavoriteRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = FavoriteRecipeModel
        fields = fields = ('id', 'name', 'image', 'cooking_time')


class ListRecipeUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField('check_if_is_subscribed')

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def check_if_is_subscribed(self, user):
        current_user = self.context['request'].user
        other_user = user.following.all()
        if other_user.count() == 0:
            return False
        if FollowModel.objects.filter(user=user, author=current_user).exists():
            return True
        return False


class AddIngredientInRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AddIngredientInRecModel
        fields = '__all__'


class IngredientInRecipeSerializerToCreateRecipe(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = AddIngredientInRecModel
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class ListRecipeSerializer(serializers.ModelSerializer):
    author = ListRecipeUserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = RecipeModel
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_ingredients(self, obj):
        qs = AddIngredientInRecModel.objects.filter(recipe=obj)
        return IngredientInRecipeSerializerToCreateRecipe(qs, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None:
            return False
        user = request.user
        return FavoriteRecipeModel.objects.filter(recipe=obj, user=user).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None:
            return False
        user = request.user
        return ShoppingListModel.objects.filter(recipe=obj, user=user).exists()


class RecipeSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        max_length=None,
        required=True,
        allow_empty_file=False,
        use_url=True,
    )
    author = ListRecipeUserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)

    class Meta:
        model = RecipeModel
        fields = '__all__'


class ShowFollowerRecipeSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        max_length=None,
        required=True,
        allow_empty_file=False,
        use_url=True,
    )

    class Meta:
        model = RecipeModel
        fields = ('id', 'name', 'image', 'cooking_time')


class ShowFollowersSerializer(serializers.ModelSerializer):

    recipes = ShowFollowerRecipeSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField('count_author_recipes')
    is_subscribed = serializers.SerializerMethodField('check_if_subscribed')

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def count_author_recipes(self, user):
        return len(user.recipes.all())

    def check_if_subscribed(self, user):
        current_user = self.context.get('current_user')
        other_user = user.following.all()
        if user.is_anonymous:
            return False
        if other_user.count() == 0:
            return False
        if FollowModel.objects.filter(user=user, author=current_user).exists():
            return True
        return False


class ShowIngredientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = IngredientModel
        fields = ('id', 'amount', )


class AddIngredientToRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=IngredientModel.objects.all())

    class Meta:
        model = AddIngredientInRecModel
        fields = ('id', 'amount')


class ShowRecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializerModified(read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = RecipeModel
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_ingredients(self, obj):
        qs = AddIngredientInRecModel.objects.filter(recipe=obj)
        return AddIngredientInRecipeSerializer(qs, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None:
            return False
        user = request.user
        return FavoriteRecipeModel.objects.filter(recipe=obj, user=user).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None:
            return False
        user = request.user
        return ShoppingListModel.objects.filter(recipe=obj, user=user).exists()


class CreateRecipeSerializer(serializers.ModelSerializer):
    image = ImageField(max_length=None, use_url=True)
    author = UserSerializerModified(read_only=True)
    ingredients = AddIngredientToRecipeSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=TagModel.objects.all(), many=True
    )

    class Meta:
        model = RecipeModel
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        author = self.context.get('request').user
        tags_data = validated_data.pop('tags')
        recipe = RecipeModel.objects.create(
            author=author, **validated_data)
        recipe.save()
        recipe.tags.set(tags_data)
        for ingredient in ingredients_data:
            ingredient_model = ingredient['id']
            amount = ingredient['amount']
            AddIngredientInRecModel.objects.create(
                ingredient=ingredient_model,
                recipe=recipe,
                amount=amount
            )

        return recipe

    def update(self, instance, validated_data):
        ingredient_data = validated_data.pop('ingredients')
        AddIngredientInRecModel.objects.filter(recipe=instance).delete()
        for new_ingredient in ingredient_data:
            AddIngredientInRecModel.objects.create(
                ingredient=new_ingredient['id'],
                recipe=instance,
                amount=new_ingredient['amount'],
            )
        instance.name = validated_data.pop('name')
        instance.text = validated_data.pop('text')
        instance.image = validated_data.pop('image')
        instance.cooking_time = validated_data.pop('cooking_time')
        instance.save()
        return instance

    def to_representation(self, instance):
        return ShowRecipeSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }
        ).data

from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
    PrimaryKeyRelatedField,
    ReadOnlyField,
    SerializerMethodField
)
from rest_framework.generics import get_object_or_404

from users.serializers import UserSerializer

from .fields import Base64ImageField
from .models import AddIngredientInRec, Ingredient, Recipe, Tag


class TagSerializer(ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientReadSerializer(ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
        read_only_fields = ('id', 'name', 'measurement_unit')


class IngredientWriteSerializer(ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'amount')


class FavoriteRecipeSerializer(ModelSerializer):

    class Meta:
        model = Recipe
        fields = fields = ('id', 'name', 'image', 'cooking_time')

    def validate(self, attrs):
        user = self.context.get('request').user
        recipe = attrs['recipe']
        method = attrs['method']
        method_ask = {
            'is_favorited': {
                'check': user.is_favorited.filter(recipe=recipe).exists(),
                'text_error_get': 'Этот рецепт уже есть в избранном',
                'text_error_delete': 'Этого рецепта не было в вашем избранном'
            },
            'is_in_shopping_cart': {
                'check': (
                    user.is_in_shopping_cart.filter(recipe=recipe).exists()
                ),
                'text_error_get': 'Этот рецепт уже есть в списке покупок',
                'text_error_delete': (
                    'Этого рецепта не было '
                    'в вашем списке покупок')
            }
        }

        if (self.context.get('request').method == 'GET'
            and method_ask[method]['check']):
            raise ValidationError(method_ask[method]['text_error_get'])

        if (self.context.get('request').method == 'DELETE'
            and not method_ask[method]['check']):
            raise ValidationError(method_ask[method]['text_error_delete'])

        return attrs


class RecipeIngredientReadSerializer(ModelSerializer):
    id = ReadOnlyField(source='ingredient.id')
    name = ReadOnlyField(source='ingredient.name')
    measurement_unit = ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = AddIngredientInRec
        fields = ('id', 'name', 'amount', 'measurement_unit')
        read_only_fields = ('amount',)


class RecipeReadSerializer(ModelSerializer):
    author = UserSerializer(read_only=True)
    ingredients = RecipeIngredientReadSerializer(source='amounts', many=True)
    tags = TagSerializer(many=True, read_only=True)
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',
            'name',
            'text',
            'image',
            'ingredients',
            'tags',
            'cooking_time',
            'is_favorited',
            'is_in_shopping_cart',
        )

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return obj.is_favorited.filter(user=user).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return obj.is_in_shopping_cart.filter(user=user).exists()


class RecipeWriteSerializer(ModelSerializer):
    author = UserSerializer(read_only=True)
    image = Base64ImageField(max_length=None, use_url=True)
    ingredients = IngredientWriteSerializer(many=True)
    tags = PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',
            'name',
            'text',
            'image',
            'ingredients',
            'tags',
            'cooking_time',
        )

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        ingredients_set = set()
        for ingredient in ingredients_data:
            if ingredient['amount'] < 0:
                raise ValidationError(
                    'Количество должно быть >= 0'
                )
            if ingredient['id'] in ingredients_set:
                raise ValidationError(
                    'Ингредиент в рецепте не должен повторяться.'
                )
            ingredients_set.add(ingredient['id'])
        recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients_data:
            amount = ingredient['amount']
            id = ingredient['id']
            AddIngredientInRec.objects.create(
                ingredient=get_object_or_404(Ingredient, id=id),
                recipe=recipe, amount=amount
            )
        for tag in tags_data:
            recipe.tags.add(tag)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.image = validated_data.get('image', instance.image)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        ingredients_set = set()
        for ingredient in ingredients_data:
            if ingredient['amount'] < 0:
                raise ValidationError(
                    'Количество должно быть >= 0'
                )
            if ingredient['id'] in ingredients_set:
                raise ValidationError(
                    'Ингредиент в рецепте не должен повторяться.'
                )
            ingredients_set.add(ingredient['id'])
        AddIngredientInRec.objects.filter(recipe=instance).delete()
        for ingredient in ingredients_data:
            amount = ingredient['amount']
            id = ingredient['id']
            AddIngredientInRec.objects.create(
                ingredient=get_object_or_404(Ingredient, id=id),
                recipe=instance, amount=amount
            )
        for tag in tags_data:
            instance.tags.add(tag)
        instance.save()
        return instance

    def to_representation(self, instance):
        data = RecipeReadSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data
        return data

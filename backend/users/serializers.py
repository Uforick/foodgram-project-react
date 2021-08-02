from django.contrib.auth import get_user_model
from rest_framework.serializers import (
    ValidationError,
    SerializerMethodField,
    ImageField,
)

from recipes.models import Recipe

User = get_user_model()


class UserSerializer(SerializerMethodField):
    is_subscribed = SerializerMethodField()

    class Meta:
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_subscribed',
            'password'
        )
        model = User
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return obj.subscriber.filter(user=user).exists()


class FollowRecipeSerializer(SerializerMethodField):
    image = ImageField(
        max_length=None,
        required=True,
        allow_empty_file=False,
        use_url=True,
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class SubRecipeSerializer(SerializerMethodField):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(SerializerMethodField):
    recipes = SerializerMethodField()
    recipes_count = SerializerMethodField()
    is_subscribed = SerializerMethodField()

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

    def validate(self, attrs):
        user = self.context.get('request').user
        author = attrs['author']
        if (self.context.get('request').method == 'GET'
            and (author == user
            or user.subscribed_on.filter(author=author).exists())):
            raise ValidationError(
                'Вы или уже подписаны на этого автора, '
                'или пытаетесь подписаться на себя, что невозможно')

        if (self.context.get('request').method == 'DELETE'
            and not user.subscribed_on.filter(author=author).exists()):
            raise ValidationError(
                'Вы не подписаны на данного автора '
                '(напоминание: на себя подписаться невозможно)'
            )

        return attrs

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return obj.subscriber.filter(user=user).exists()

    def get_recipes(self, obj):
        request = self.context['request']
        limit = int(request.query_params.get('recipes_limit', 3))
        recipes = obj.recipes.all()[:limit]
        serializer = SubRecipeSerializer(
            recipes,
            many=True,
            context={'request': request},
        )
        serializer.is_valid()
        return serializer.data

    def get_recipes_count(self, obj):
        return obj.recipes.all().count()

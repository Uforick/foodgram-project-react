from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from .models import CustomUser as User
from .models import Follow
from recipes.models import RecipeModel


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'password',
            'first_name',
            'last_name'
        )


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'password',
            'first_name',
            'last_name'
        )


class FollowRecipeSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        max_length=None,
        required=True,
        allow_empty_file=False,
        use_url=True,
    )

    class Meta:
        model = RecipeModel
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class FollowSerializer(serializers.ModelSerializer):
    recipes = FollowRecipeSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField('count_author_recipes')
    is_subscribed = serializers.SerializerMethodField('if_subscribed')

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name'
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def count_author_recipes(self, user):
        return len(user.recipes.all())

    def if_subscribed(self, user):
        current_user = self.context.get('current_user')
        other_user = user.following.all()
        if user.is_anonymous:
            return False
        if other_user.count() == 0:
            return False
        if Follow.objects.filter(user=user, following=current_user).exists():
            return True
        return False

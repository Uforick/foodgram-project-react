from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import filters, viewsets

from .models import RecipeModel, TagModel, IngredientModel
from . import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = RecipeModel.objects.all()
    serializer_class = serializers.RecipeSerializer
    http_method_names = ('get', 'post', 'put', 'delete')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    queryset = TagModel.objects.all()
    serializer_class = serializers.TagSerializer
    http_method_names = ('get',)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = IngredientModel.objects.all()
    serializer_class = serializers.IngredientSerializer
    http_method_names = ('get',)

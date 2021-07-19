from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import filters, viewsets

from .models import RecipeModel, TagModel, IngredientModel


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = RecipeModel.objects.all()
    http_method_names = ('get', 'post', 'put', 'delete')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    queryset = TagModel.objects.all()
    http_method_names = ('get',)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = IngredientModel.objects.all()
    http_method_names = ('get',)
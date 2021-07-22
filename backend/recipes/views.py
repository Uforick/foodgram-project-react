# from django.contrib.auth.decorators import login_required
# from django.core.paginator import Paginator
# from django.conf import settings
# from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.decorators import permission_classes
from rest_framework import filters, status, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import RecipeModel, TagModel, IngredientModel
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

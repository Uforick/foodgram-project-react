from django.shortcuts import get_object_or_404
from djoser.serializers import SetPasswordSerializer
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import CustomUser, FollowModel
from .permissions import IsOwnerOrAdmin
from .serializers import FollowSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        serializer.save()
        user = get_object_or_404(CustomUser, username=username)
        user.set_password(password)
        user.save()

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        serializer = self.get_serializer(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False,
            methods=['post'],
            permission_classes=[IsOwnerOrAdmin])
    def set_password(self, request, *args, **kwargs):
        serializer = SetPasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        new_password = serializer.validated_data['new_password']
        self.request.user.set_password(new_password)
        self.request.user.save()
        return Response(data={}, status=status.HTTP_201_CREATED)

    @action(detail=False,
            methods=['get'],
            permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        queryset = CustomUser.objects.filter(
            subscriber__user=request.user).order_by('id')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = FollowSerializer(
                page, many=True, context={'request': request}
            )
            return self.get_paginated_response(serializer.data)
        serializer = FollowSerializer(
            page, many=True, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True,
            methods=['get', 'delete'],
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, pk):
        author = get_object_or_404(CustomUser, pk=pk)
        user = request.user
        subscribed = user.subscribed_on.filter(author=author).exists()
        if request.method == 'GET':
            if author != user and not subscribed:
                FollowModel.objects.create(user=user, author=author)
                serializer = UserSerializer(
                    author,
                    context={'request': request}
                )
                return Response(data=serializer.data,
                                status=status.HTTP_201_CREATED)
            data = {
                'errors': ('Вы или уже подписаны на этого автора, '
                           'или пытаетесь подписаться на себя, что невозможно')
            }
            return Response(data=data, status=status.HTTP_403_FORBIDDEN)
        if not user.subscribed_on.filter(author=author).exists():
            data = {
                'errors': ('Вы не подписаны на данного автора '
                           '(напоминание: на себя подписаться невозможно)')
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        FollowModel.objects.filter(user=user, author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

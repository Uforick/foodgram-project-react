from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomUser, FollowModel
from .serializers import FollowSerializer, UserSerializer


@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def whofollows(request):
    users = request.user.user.all()
    user_obj = [follow_obj.following for follow_obj in users]
    paginator = PageNumberPagination()
    paginator.page_size = 10
    result_page = paginator.paginate_queryset(user_obj, request)
    serializer = FollowSerializer(
        result_page, many=True, context={'current_user': request.user})
    return paginator.get_paginated_response(serializer.data)


class FollowViewSet(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, user_id):
        user = request.user
        following = get_object_or_404(CustomUser, id=user_id)
        if FollowModel.objects.filter(user=user, following=following).exists():
            return Response(
                'Вы уже подписаны',
                status=status.HTTP_400_BAD_REQUEST
            )
        FollowModel.objects.create(user=user, following=following)
        serializer = UserSerializer(following)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, user_id):
        user = request.user
        following = get_object_or_404(CustomUser, id=user_id)
        try:
            follow = get_object_or_404(user=user, following=following)
            follow.delete()
            return Response(
                'Удалено',
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception:
            return Response(
                'Подписки не было',
                status=status.HTTP_400_BAD_REQUEST
            )

from django.urls import include, path
from .views import whofollows, FollowViewSet

urlpatterns = [
    path(
        'users/subscriptions/',
        whofollows,
        name='users_subs'
    ),
    path(
        'users/<int:user_id>/subscribe/',
        FollowViewSet.as_view(),
        name='subscribe'
    ),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

]

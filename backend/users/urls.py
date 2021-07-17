from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter
from .views import UserProfileDetailView, UserProfileListView, FollowViewSet

router = DefaultRouter()


router.register(
    r'follow',
    FollowViewSet,
    basename='follow'
)


urlpatterns = [
    path('', UserProfileListView.as_view(), name='all-profiles'),
    path('<int:pk>/', UserProfileDetailView.as_view(), name='profile'),
    path('', include(router.urls))

]

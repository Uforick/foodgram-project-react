from django.urls import include, path
from .views import UserProfileDetailView, UserProfileListView


urlpatterns = [
    path('set_password/', include('djoser.urls')),
    path('', UserProfileListView.as_view(), name='all-profiles'),
    path('<int:pk>/', UserProfileDetailView.as_view(), name='profile'),
    path('me/', UserProfileDetailView.as_view(), name='my_profile'),

]

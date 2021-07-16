from django.urls import path
from .views import UserProfileDetailView, UserProfileListView


urlpatterns = [
    path('', UserProfileListView.as_view(), name='all-profiles'),
    path('<int:pk>/', UserProfileDetailView.as_view(), name='profile'),

]

from django.urls import path
from .views import UserListCreateView, UserDetailView, MeView, GroupListView, GroupCreateView, GroupDetailView


urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list'),
    path('users/', UserListCreateView.as_view(), name='user-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('me/', MeView.as_view(), name='me'),

    path('groups/', GroupListView.as_view(), name='group-list'),
    path('groups/', GroupCreateView.as_view(), name='group-create'),
    path('groups/<int:pk>/', GroupDetailView.as_view(), name='group-detail'),
]
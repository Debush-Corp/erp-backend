from django.urls import path
from .views import (
    UserListCreateView,
    UserDetailView,
    ValidateFieldView,
    MeView,
    GroupListCreateView,
    GroupDetailView
)

urlpatterns = [
    # endpoints de usuarios
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('users/validate/', ValidateFieldView.as_view(), name='user-field-validate'),
    path('me/', MeView.as_view(), name='me'),  # Perfil del usuario autenticado

    # endpoints de grupos
    path('groups/', GroupListCreateView.as_view(), name='group-list-create'),
    path('groups/<int:pk>/', GroupDetailView.as_view(), name='group-detail'),
]
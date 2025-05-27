from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .serializers import UserSerializer, UserCreateSerializer, UserUpdateSerializer, GroupSerializer

User = get_user_model()

# Permiso personalizado: admin o el propio usuario
class IsAdminOrSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj == request.user

# Vista para listar y crear usuarios
class UserListCreateView(generics.ListCreateAPIView):
    """
    GET /api/users/ - Lista todos los usuarios (solo admins)
    POST /api/users/ - Crea un nuevo usuario (solo admins)
    """
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserSerializer

# Vista para detalles, actualización y eliminación de usuarios
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/users/<id>/ - Detalles del usuario (admin o propio)
    PUT /api/users/<id>/ - Actualiza el usuario (admin o propio)
    DELETE /api/users/<id>/ - Elimina el usuario (solo admins)
    """
    queryset = User.objects.all()
    permission_classes = [IsAdminOrSelf]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserSerializer

# Vista para el perfil del usuario autenticado
class MeView(generics.RetrieveUpdateAPIView):
    """
    GET /api/me/ - Detalles del usuario autenticado
    PUT /api/me/ - Actualiza el perfil del usuario autenticado
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserSerializer

# Vista para listar y crear grupos
class GroupListCreateView(generics.ListCreateAPIView):
    """
    GET /api/groups/ - Lista todos los grupos (solo admins)
    POST /api/groups/ - Crea un nuevo grupo (solo admins)
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser]

# Vista para detalles, actualización y eliminación de grupos
class GroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/groups/<id>/ - Detalles del grupo (solo admins)
    PUT /api/groups/<id>/ - Actualiza el grupo (solo admins)
    DELETE /api/groups/<id>/ - Elimina el grupo (solo admins)
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser]
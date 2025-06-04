from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import UserActivity
from .serializers import UserSerializer, MeSerializer, GroupSerializer
from pagination import SmallPagination, MediumPagination, LargePagination, ExtraLargePagination

User = get_user_model()

# Permiso personalizado: admin o el propio usuario
class IsAdminOrSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj == request.user

# Vista para listar usuarios (solo admins)
class UserListCreateView(generics.ListCreateAPIView):
    """
    GET /api/accounts/users/ - Lista usuarios (solo admins)
    POST /api/accounts/users/ - Crea un nuevo usuario (solo admins)
    """
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = SmallPagination

# Vista para detalles, actualización y eliminación de usuarios
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/accounts/users/<id>/ - Detalles del usuario (admin o propio)
    PUT /api/accounts/users/<id>/ - Actualiza el usuario (admin o propio)
    DELETE /api/accounts/users/<id>/ - Elimina el usuario (solo admins)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrSelf]

    def perform_destroy(self, instance):
        UserActivity.objects.create(
            user=self.request.user,
            action="delete_user",
            description=f"Eliminó al usuario {instance.username}",
            module="users"
        )
        instance.delete()

# Vista para listar grupos (solo admins)
class GroupListView(generics.ListAPIView):
    """
    GET /api/accounts/groups/ - Lista todos los grupos (solo admins)
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = MediumPagination

class GroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/accounts/groups/<id>/ - Detalles del rol (solo admins)
    PUT /api/accounts/groups/<id>/ - Actualiza el rol (solo admins)
    DELETE /api/accounts/groups/<id>/ - Elimina el rol (solo admins)
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

# Vista para crear grupo (solo admins)
class GroupCreateView(generics.CreateAPIView):
    """
    POST /api/accounts/groups/ - Crea un nuevo grupo (solo admins)
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAdminUser]

# Vista para el perfil del usuario autenticado
class MeView(generics.RetrieveUpdateAPIView):
    """
    GET /api/accounts/me/ - Detalles del usuario autenticado
    PUT /api/accounts/me/ - Actualiza el perfil del usuario autenticado
    """
    serializer_class = MeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
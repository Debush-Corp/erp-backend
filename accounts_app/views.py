from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from .models import UserActivity
from .serializers import UserSerializer, MeSerializer, GroupSerializer
from pagination import SmallPagination

User = get_user_model()


# Vista para listar y crear usuarios
class UserListCreateView(generics.ListCreateAPIView):
    """
    GET /api/accounts/users/ - Lista usuarios (solo admins)
    POST /api/accounts/users/ - Crea un nuevo usuario (solo admins)
    """
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    pagination_class = SmallPagination


# Vista para obtener, actualizar y eliminar un usuario
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/accounts/users/<id>/ - Detalles del usuario (admin o propio)
    PUT /api/accounts/users/<id>/ - Actualiza el usuario (admin o propio)
    DELETE /api/accounts/users/<id>/ - Elimina el usuario (solo admins)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.DjangoModelPermissions]

    def perform_destroy(self, instance):
        UserActivity.objects.create(
            user=self.request.user,
            action="delete_user",
            description=f"Eliminó al usuario {instance.username}",
            module="users"
        )
        instance.delete()


# Vista para obtener el usuario autenticado (tipo perfil)
class MeView(APIView):
    """
    GET /api/accounts/me/ - Retorna los datos del usuario autenticado
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = MeSerializer(request.user)
        return Response(serializer.data)


# Vista para listar y crear grupos
class GroupListCreateView(generics.ListCreateAPIView):
    """
    GET /api/accounts/groups/ - Lista todos los grupos
    POST /api/accounts/groups/ - Crea un nuevo grupo
    """
    queryset = Group.objects.all().order_by('id')
    serializer_class = GroupSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    pagination_class = SmallPagination


# Vista para detalles de grupo
class GroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/accounts/groups/<id>/ - Detalles del grupo
    PUT /api/accounts/groups/<id>/ - Actualiza el grupo
    DELETE /api/accounts/groups/<id>/ - Elimina el grupo
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.DjangoModelPermissions]
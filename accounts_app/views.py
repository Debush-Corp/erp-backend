from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import FieldDoesNotExist
import re

from .models import UserActivity
from .serializers import UserSerializer, MeSerializer, GroupSerializer
from pagination import SmallPagination

User = get_user_model()

# Vista para validar fields
class ValidateFieldView(APIView):
    """
    POST /api/accounts/users/validate/ - Valida un campo único del modelo User
    Expects: { "field": string, "value": string }
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        field = request.data.get('field', '').strip()
        value = request.data.get('value', '').strip()

        print(f"Recibiendo del backend: field={field}, value={value}")

        # Validar que se proporcionen ambos parámetros
        if not field or not value:
            return Response(
                {'valid': False, 'error_code': 'invalid_request', 'error': 'Se requieren los campos "field" y "value".'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Verificar si el campo existe en el modelo User
            User._meta.get_field(field)

            # Crear el filtro dinámico
            filter_kwargs = {field: value}

            # Verificar si el valor ya existe
            if User.objects.filter(**filter_kwargs).exists():
                return Response(
                    {'valid': False, 'error_code': 'duplicate', 'error': f'El {field} ingresado ya existe.'},
                    status=status.HTTP_200_OK
                )
            return Response(
                {'valid': True, 'message': f'{field.capitalize()} disponible.'},
                status=status.HTTP_200_OK
            )
        except FieldDoesNotExist:
            return Response(
                {'valid': False, 'error_code': 'invalid_field', 'error': f'El campo {field} no es válido.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            print(f"Error en el servidor: {str(e)}")
            return Response(
                {'valid': False, 'error_code': 'error', 'error': 'Error en el servidor.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
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
    PATCH /api/accounts/users/<id>/ - Actualiza parcialmente el usuario (admin o propio)
    DELETE /api/accounts/users/<id>/ - Elimina el usuario (solo admins)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.DjangoModelPermissions]

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        print(f"[GET] Usuario: {serializer.data}")
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        if request.method == "PUT":
            print(f"[PUT] Datos recibidos: {request.data}")
        else:
            print(f"[PATCH dentro de update()] Datos recibidos: {request.data}")
        return super().update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        print(f"[PATCH] Datos recibidos: {request.data}")
        return super().partial_update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        username = instance.username
        self.perform_destroy(instance)
        print(f"[DELETE] Usuario eliminado: {username}")
        return Response(status=status.HTTP_204_NO_CONTENT)

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
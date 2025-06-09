from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .serializers import PasswordRequestSerializer
from .utils import generate_password

class GeneratePasswordView(generics.CreateAPIView):
    """
    POST /password/api/generate/ - Genera una contraseña según los parámetros proporcionados
    """
    serializer_class = PasswordRequestSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requiere autenticación

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            length = serializer.validated_data['length']
            use_uppercase = serializer.validated_data['use_uppercase']
            use_lowercase = serializer.validated_data['use_lowercase']
            use_digits = serializer.validated_data['use_digits']
            use_special = serializer.validated_data['use_special']
            
            password, error = generate_password(length, use_uppercase, use_lowercase, use_digits, use_special)
            if error:
                return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'password': password}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
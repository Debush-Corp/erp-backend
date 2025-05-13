from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import CustomTokenObtainPairSerializer, UserSerializer

class LoginView(TokenObtainPairView):
    """
    POST /api/auth/login/ 
    body: { username, password }
    """
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]

class RefreshView(TokenRefreshView):
    """
    POST /api/auth/refresh/
    body: { refresh }
    """
    permission_classes = [permissions.AllowAny]

class LogoutView(APIView):
    """
    POST /api/auth/logout/
    body: { refresh }
    Revoca el refresh token (usa blacklist).
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            token = RefreshToken(request.data['refresh'])
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class MeView(APIView):
    """
    GET /api/auth/me/
    Devuelve datos básicos del usuario autenticado.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
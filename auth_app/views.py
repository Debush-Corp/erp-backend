from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from accounts_app.models import UserActivity
from accounts_app.serializers import UserSerializer
from .serializers import CustomTokenObtainPairSerializer

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
    Revoca el refresh token y actualiza is_online.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            token = RefreshToken(request.data['refresh'])
            token.blacklist()
            request.user.is_online = False
            request.user.save()
            UserActivity.objects.create(
                user=request.user,
                action='logout',
                description=f'Usuario {request.user.username} finalizó actividad',
                module='auth_app'
            )
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
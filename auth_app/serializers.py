from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Valida username/password y genera access + refresh.
    Aquí añadimos campos extra al payload de la respuesta.
    """
    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({
            'user_id': self.user.id,
            'username': self.user.username,
            # puedes añadir email, roles, lo que necesites…
        })
        return data

class UserSerializer(serializers.ModelSerializer):
    """
    Para devolver los datos del usuario en /me/
    """
    class Meta:
        model = User
        fields = ('username', 'groups')
        read_only_fields = fields

    def get_groups(self, obj):
        return list(obj.groups.values_list('name', flat=True))
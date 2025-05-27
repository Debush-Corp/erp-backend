from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

# Serializer para listar y obtener detalles de usuarios
class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(many=True, slug_field='name', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'groups']

# Serializer para crear usuarios
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    groups = serializers.PrimaryKeyRelatedField(many=True, queryset=Group.objects.all(), required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'groups']

    def create(self, validated_data):
        groups = validated_data.pop('groups', [])
        user = User.objects.create_user(**validated_data)
        user.groups.set(groups)
        return user

# Serializer para actualizar usuarios
class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    groups = serializers.PrimaryKeyRelatedField(many=True, queryset=Group.objects.all(), required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'groups']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si el usuario no es admin, eliminamos el campo 'groups' para que no pueda modificarlo
        if not self.context['request'].user.is_staff:
            self.fields.pop('groups', None)

    def update(self, instance, validated_data):
        groups = validated_data.pop('groups', None)
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()

        # Solo actualizamos los grupos si el usuario es admin y se proporcionaron grupos
        if groups is not None and self.context['request'].user.is_staff:
            instance.groups.set(groups)

        return instance

# Serializer para gestionar grupos
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import UserActivity

User = get_user_model()

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

class SimpleGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']

class UserSerializer(serializers.ModelSerializer):
    group_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'password', 'first_name', 'last_name',
            'email', 'document', 'date_joined', 'is_active',
            'last_login', 'groups', 'group_ids'
        ]
        read_only_fields = ['id', 'date_joined', 'is_active', 'last_login', 'groups']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_group_ids(self, value):
        if value:
            valid_groups = Group.objects.filter(id__in=value).values_list('id', flat=True)
            invalid_ids = set(value) - set(valid_groups)
            if invalid_ids:
                raise serializers.ValidationError(f"Los siguientes IDs de grupos no existen: {invalid_ids}")
        return value

    def create(self, validated_data):
        group_ids = validated_data.pop('group_ids', [])
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        if group_ids:
            try:
                user.groups.set(group_ids)
            except Exception as e:
                raise serializers.ValidationError(f"Error al asignar grupos: {str(e)}")
        return user

    def update(self, instance, validated_data):
        group_ids = validated_data.pop('group_ids', [])
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        if group_ids:
            try:
                instance.groups.set(group_ids)
            except Exception as e:
                raise serializers.ValidationError(f"Error al asignar grupos: {str(e)}")

        return instance

class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        fields = '__all__'
        read_only_fields = ['id', 'timestamp']

class MeSerializer(serializers.ModelSerializer):
    groups = SimpleGroupSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name',
            'email', 'document', 'date_joined', 'last_login', 'groups'
        ]
        read_only_fields = fields
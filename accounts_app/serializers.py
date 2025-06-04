from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import UserActivity

User = get_user_model()

# Serializer para auth_group
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

# Serializer para auth_user
class UserSerializer(serializers.ModelSerializer):
    group_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'date_joined', 'is_active', 'last_login', 'groups', 'group_ids']
        read_only_fields = ['id', 'date_joined', 'is_active', 'last_login', 'groups']

    def create(self, validated_data):
        group_ids = validated_data.pop('group_ids', [])
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        if group_ids:
            user.groups.set(Group.objects.filter(id__in=group_ids))
        return user

    def update(self, instance, validated_data):
        group_ids = validated_data.pop('group_ids', None)
        allowed_fields = ['username', 'first_name', 'last_name', 'email', 'is_active']
        for field in allowed_fields:
            if field in validated_data:
                setattr(instance, field, validated_data[field])
        if group_ids is not None:
            instance.groups.set(Group.objects.filter(id__in=group_ids))
        instance.save()
        return instance
    
class MeSerializer(serializers.ModelSerializer):
    groups = SimpleGroupSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'groups']
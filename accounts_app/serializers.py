from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils.timezone import localtime
from .models import UserActivity

User = get_user_model()

class GroupSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ['id', 'name']
        read_only_fields = ['id']

    def get_name(self, obj):
        nombres = {
            'system_admin': 'Administrador del Sistema',
            'general_manager': 'Gerente General',
            'sales_analyst': 'Analista de Ventas',
            # etc...
        }
        return nombres.get(obj.name, obj.name.replace('_', ' ').title())

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

class SimpleGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']

class UserSerializer(serializers.ModelSerializer):
    group_ids = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        write_only=True,
        many=True,
        required=False
    )
    roles = GroupSerializer(many=True, read_only=True, source='groups')
    last_login = serializers.SerializerMethodField()
    date_joined = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'password', 'first_name', 'last_name',
            'email', 'document', 'date_joined', 'last_login',
            'is_active', 'roles', 'group_ids'
        ]
        read_only_fields = [
            'id', 'date_joined', 'last_login',
            'is_active', 'roles'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def _format_datetime(self, dt):
        if not dt:
            return None
        dt = localtime(dt)
        return {
            'day': f"{dt.day:02}",
            'month': f"{dt.month:02}",
            'year': dt.year,
            'hours': f"{dt.hour:02}",
            'minutes': f"{dt.minute:02}",
        }

    def get_last_login(self, obj):
        return self._format_datetime(obj.last_login)

    def get_date_joined(self, obj):
        return self._format_datetime(obj.date_joined)

    def create(self, validated_data):
        group_ids = validated_data.pop('group_ids', [])
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        user.groups.set(group_ids)
        return user

    def update(self, instance, validated_data):
        group_ids = validated_data.pop('group_ids', None)
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        if group_ids is not None:
            instance.groups.set(group_ids)
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
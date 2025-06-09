from rest_framework import serializers

class PasswordRequestSerializer(serializers.Serializer):
    length = serializers.IntegerField(min_value=6, max_value=50)
    use_uppercase = serializers.BooleanField(default=False)
    use_lowercase = serializers.BooleanField(default=False)
    use_digits = serializers.BooleanField(default=False)
    use_special = serializers.BooleanField(default=False)
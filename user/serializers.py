import string
import random
from .models import TemporaryManager
from rest_framework import serializers
from .models import User


class ManagerCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password', self.generate_random_password())
        user = User.objects.create_user(
            **validated_data,
            password=password,
            role='manager'
        )
        # 👉 TemporaryManager modelga yozamiz
        TemporaryManager.objects.create(user=user, raw_password=password)
        return user

    def generate_random_password(self, length=12):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from .models import User


class RegisterUserSerializer(WritableNestedModelSerializer):
    email = serializers.EmailField(required=True, allow_null=False, allow_blank=False)
    password = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    birth_date = serializers.DateField(format='d.m.YYYY',required=True)

    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    patronymic = serializers.CharField(required=False)

    avatar = serializers.CharField(required=False)

    def create(self, validated_data):
        try:
            password = validated_data.pop('password')
            instance = User(**validated_data)
            instance.set_password(password)
            instance.is_active = True
            instance.save()

            return instance
        except TypeError as e:
            raise TypeError("Type Error While Create")

    class Meta:
        model = User
        fields = ('email', 'password', 'birth_date',
                  'first_name', 'last_name', 'patronymic',
                  'avatar')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'birth_date',
                  'first_name', 'last_name', 'patronymic',
                  'avatar')

from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer, RegisterUserSerializer
from core.mixins.upload_mixin import UploadMixin


class UserViewSet(viewsets.ModelViewSet, UploadMixin):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        instance = request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
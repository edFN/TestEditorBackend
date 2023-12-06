import os.path

from rest_framework import decorators, status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from core.serializers.serializer import UploadSerializer


class UploadMixin:
    @decorators.action(detail=False, methods=['post'], serializer_class=UploadSerializer,
                       parser_classes=[MultiPartParser, ])
    def upload(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            file = serializer.save()

            print("FileInstance", os.path.basename(file))

            return Response(os.path.basename(file), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

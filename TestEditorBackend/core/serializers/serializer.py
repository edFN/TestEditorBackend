from django.core.files.storage import default_storage
from rest_framework import serializers


class UploadSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)

    def get_file(self, obj):
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(obj.file.url)
        else:
            return obj.file.url

    def save(self):
        file = self.validated_data['file']
        file_name = default_storage.save(file.name, file)
        print('file_name: ', default_storage.url(file_name))
        request = self.context.get('request')
        if request is not None:
            print(request.build_absolute_uri(default_storage.url(file_name)))
            return request.build_absolute_uri(default_storage.url(file_name))
        else:
            return default_storage.url(file_name)

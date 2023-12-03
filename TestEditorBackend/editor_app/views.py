from django.shortcuts import render

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from .admin import TestModel
from .models import MessageFinishedTest, HashTagsModel, TypeTestModel
from .serializers.presenter.serializers import TestSerializerPresenter, AnswerSetValidatorSerializer, HashTagsSerializer
from .serializers.write.serializers import TestSerializerWriter
from core.mixins.upload_mixin import UploadMixin

from .services.check_correct_answers import AnswerCheckService
from .utils import get_message_points, MyMetaData

from django_filters import rest_framework as filters


class TestFilter(filters.FilterSet):
    created_at_in = filters.DateFilter(field_name='created_at', lookup_expr='gte', input_formats=['%d/%m/%Y'])
    created_at_out = filters.DateFilter(field_name='created_at', lookup_expr='lte',input_formats=['%d/%m/%Y'])
    type = filters.CharFilter(field_name='type', method="filter_type")
    class Meta:
        model = TestModel
        fields = ['is_private', 'type', 'created_at_in', 'created_at_out']

    def filter_type(self, queryset, name, value):
        print(value)

        types = value.split(',') if value else []
        return queryset.filter(type__in=types)

class HashTagViewSet(viewsets.ModelViewSet):
    serializer_class = HashTagsSerializer
    filter_backends = [SearchFilter]
    search_fields = ["name"]
    queryset = HashTagsModel.objects.all()

class TestViewSet(viewsets.ModelViewSet, UploadMixin):
    serializer_class = TestSerializerPresenter
    queryset = TestModel.objects.all()
    metadata_class = MyMetaData

    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title', 'description']
    filterset_class = TestFilter

    def create(self, request, *args, **kwargs):
        serializer = TestSerializerWriter(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['POST'])
    def accept_answers(self, request, *args, **kwargs):

        instance: TestModel = self.get_object()

        serializer = AnswerSetValidatorSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        points = AnswerCheckService.check_answers(entry=serializer.validated_data)

        data = {
            "points": points,
        }

        if instance.is_different_msg:
            print("DifferentMessage", get_message_points("points"))
            data['message'] = get_message_points(points)

        if instance.is_record_statistic:
            pass

        return Response(status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = TestSerializerWriter(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def options(self, request, *args, **kwargs):
        self.serializer_class = TestSerializerWriter
        data = super().options(request, *args, **kwargs)
        self.serializer_class = TestSerializerPresenter
        return data

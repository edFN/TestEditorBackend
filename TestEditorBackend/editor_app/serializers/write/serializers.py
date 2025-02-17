import os.path

from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from editor_app.models import TestQuestionModel, TestAnswerModel, TypeTestModel, TestModel, HashTagsModel, \
    MessageFinishedTest
from authentication.models import User


class QuestionAnswerSerializerWriter(WritableNestedModelSerializer):
    answer_image = serializers.CharField(label="Изображение", required=False, allow_null=True)
    answer_text = serializers.CharField(required=False, allow_null=True)

    class Meta:
        fields='__all__'
        model = TestAnswerModel


class TestQuestionSerializer(WritableNestedModelSerializer):
    answers = QuestionAnswerSerializerWriter(many=True, required=False, source="question_answer_rel")

    class Meta:
        model = TestQuestionModel
        fields = '__all__'


class MessageFinishedTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageFinishedTest
        fields = '__all__'


class TestSerializerWriter(WritableNestedModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)

    type = serializers.PrimaryKeyRelatedField(queryset=TypeTestModel.objects.all(), required=True)

    questions = TestQuestionSerializer(many=True, required=False, source="test_question_rel")

    image = serializers.CharField(label="Изображение", required=False, allow_null=True)

    hashtags = serializers.PrimaryKeyRelatedField(queryset=HashTagsModel.objects.all(), many=True, allow_null=True,
                                                  allow_empty=True)
    created_at = serializers.DateField(format="%d/%m/%Y", required=False)

    message_results = MessageFinishedTestSerializer(source='message_finish_rel', required=False,many=True)

    def update(self, instance, validated_data):
        if validated_data['image'] is not None:
            validated_data['image'] = os.path.basename((validated_data['image']))
        return super().update(instance, validated_data)

    class Meta:
        fields = '__all__'
        model = TestModel
        depth = 2

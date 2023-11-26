from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from editor_app.models import TestQuestionModel, TestAnswerModel, TypeTestModel, TestModel
from authentication.models import User


class QuestionAnswerSerializerWriter(WritableNestedModelSerializer):
    answer_image = serializers.CharField(label="Изображение", required=False, allow_null=True)
    answer_text = serializers.CharField(required=False, allow_null=True)

    class Meta:
        exclude = ('is_right',)
        model = TestAnswerModel



class TestQuestionSerializer(WritableNestedModelSerializer):
    answers = QuestionAnswerSerializerWriter(many=True, required=False, source="question_answer_rel")

    class Meta:
        model = TestQuestionModel
        fields = '__all__'


class TestSerializerWriter(WritableNestedModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)

    type = serializers.PrimaryKeyRelatedField(queryset=TypeTestModel.objects.all(), required=True)

    questions = TestQuestionSerializer(many=True, required=False, source="test_question_rel")

    image = serializers.CharField(label="Изображение", required=False, allow_null=True)


    class Meta:
        fields = '__all__'
        model = TestModel
        depth = 2


from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from editor_app.models import TestQuestionModel, TestAnswerModel, TypeTestModel, TestModel,HashTagsModel
from authentication.models import User
from rest_framework.exceptions import ValidationError

from editor_app.serializers.write.serializers import MessageFinishedTestSerializer


class QuestionAnswerSerializer(WritableNestedModelSerializer):
    class Meta:
        exclude = ('is_right',)
        model = TestAnswerModel


class TestQuestionSerializer(WritableNestedModelSerializer):
    answers = QuestionAnswerSerializer(many=True, required=False, source="question_answer_rel")

    class Meta:
        model = TestQuestionModel
        fields = '__all__'


class TestSerializerPresenter(WritableNestedModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)

    type = serializers.SerializerMethodField(required=False)

    created_at = serializers.DateField(format="%d/%m/%Y", required=False)

    questions = TestQuestionSerializer(many=True, required=False, source="test_question_rel")

    def get_type(self,obj):
        return obj.type.name if obj.type else ""

    class Meta:
        fields = '__all__'
        model = TestModel
        depth = 2


class HashTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashTagsModel
        fields = '__all__'

class AnswerValidatorSerializer(serializers.Serializer):
    answer_text = serializers.CharField(label="Письменный ответ", required=False, allow_blank=True, allow_null=True,
                                        )
    answer_id = serializers.PrimaryKeyRelatedField(queryset=TestAnswerModel.objects.all(), required=False, many=True)
    question_id = serializers.PrimaryKeyRelatedField(queryset=TestQuestionModel.objects.all(), required=True,
                                                     many=False)

    def validate(self, attrs):

        answer_id = attrs.get('answer_id', [])

        for answer in answer_id:
            if answer.question != attrs['question_id']:
                raise ValidationError("Id validation error")

        return super().validate(attrs)
        # raise ValidationError


class AnswerSetValidatorSerializer(serializers.Serializer):
    answers = AnswerValidatorSerializer(many=True, required=True)


class TestStandartSerializerPresenter(WritableNestedModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)

    type = serializers.PrimaryKeyRelatedField(queryset=TypeTestModel.objects.all(), required=True)

    questions = TestQuestionSerializer(many=True, required=False, source="test_question_rel")

 #   image = serializers.ImageField(label="Изображение", required=False, allow_null=True)

    hashtags = serializers.PrimaryKeyRelatedField(queryset=HashTagsModel.objects.all(), many=True, allow_null=True,
                                                  allow_empty=True)
    created_at = serializers.DateField(format="%d/%m/%Y", required=False)

    message_results = MessageFinishedTestSerializer(source='message_finish_rel',required=False,  many=True)

    class Meta:
        fields = '__all__'
        model = TestModel
        depth = 2

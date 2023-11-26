from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from editor_app.models import TestQuestionModel, TestAnswerModel, TypeTestModel, TestModel
from authentication.models import User
from rest_framework.exceptions import ValidationError


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

    type = serializers.PrimaryKeyRelatedField(queryset=TypeTestModel.objects.all(), required=True)

    questions = TestQuestionSerializer(many=True, required=False, source="test_question_rel")

    class Meta:
        fields = '__all__'
        model = TestModel
        depth = 2


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

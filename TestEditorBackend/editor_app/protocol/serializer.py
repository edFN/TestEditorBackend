from django.db.models import Q
from rest_framework import serializers

from editor_app.models import TestQuestionModel, UserAnswerRecord, ProtocolRecord, TestAnswerModel


def filter_for_choice(obj):
    return obj.question.type.name != 'TEXT'


def filter_for_text(obj):
    return not filter_for_choice(obj)


class ProtocolSerializer(serializers.ModelSerializer):
    test_answers = serializers.SerializerMethodField()
    user_answer = serializers.SerializerMethodField()

    def get_user_answer(self,obj):
        return str(obj.answer_user)
    def get_test_answers(self, obj):
        items = UserAnswerRecord.objects.filter(protocol=obj)

        if not len(items):
            return []

        output_data = []

        set_by_question = {}

        answer_choice = list(filter(filter_for_choice, items))
        text_answer = list(filter(filter_for_text, items))

        print("TestAnswer", text_answer)



        for answer in answer_choice:

            print("Answer", answer.__dict__)

            if not answer.question in set_by_question:
                set_by_question[answer.question] = [answer]
            else:
                set_by_question[answer.question].append(answer)

        for question in set_by_question.keys():
            right_answers = TestAnswerModel.objects.filter(Q(is_right=True) & Q(question=question))

            output_data.append({
                "type": "CHOICE",
                "question": question.question,
                "answers": [obj.answer_id.answer_text for obj in set_by_question[question]],
                "right_answer": [obj.answer_text for obj in right_answers]
            })

        for item in text_answer:
            right_answer = TestAnswerModel.objects.filter(Q(is_right=True) & Q(question=item.question)).first()
            output_data.append({
                "type": "TEXT",
                "question": item.question.question,
                "answer_text": item.answer_text,
                "right_answer": right_answer.answer_text,
                "answers": []
            })

        return output_data

    class Meta:
        fields = '__all__'
        model = ProtocolRecord

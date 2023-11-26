from django.db.models import Q

from editor_app.models import TestAnswerModel


class CheckStrategy:
    def check(self, entry):
        pass


class CheckOneVariant(CheckStrategy):
    def check(self, entry):
        answer = entry['answer_id'][0]

        if not answer.is_right:
            return 0

        if entry['question'].has_diff_point:
            return answer.answer_points

        return 1


class CheckMultipleVariant(CheckStrategy):
    def check(self, entry):
        answers = entry['answer_id']

        sum = 0

        for answer in answers:
            if not answer.is_right:
                return 0

            sum += answer.answer_points if entry['question_id'].has_diff_point else 1

        return sum


class CheckTextType(CheckStrategy):
    def check(self, entry):
        answer = entry['answer_text']
        question = entry['question_id']

        ok = TestAnswerModel.objects.filter(Q(question=question) & Q(answer_text=answer)).exists()

        return 1 if ok else 0


def factory_check_question_answer(type, entry):
    if type == 'ONE_VARIANT':
        return CheckOneVariant().check(entry)
    if type == 'MULTIPLE_VARIANT':
        return CheckMultipleVariant().check(entry)
    if type == 'TEXT':
        return CheckTextType().check(entry)

    raise NotImplementedError("Not implemented for type: %s" % type)


class AnswerCheckService:
    @staticmethod
    def check_answers(entry):
        points = 0
        for answer in entry['answers']:
            points += factory_check_question_answer(answer['question_id'].type, entry)

        return points

from editor_app.models import TestQuestionModel

from editor_app.models import UserAnswerRecord

from editor_app.models import ProtocolRecord


class RecordStatisticService:
    @staticmethod
    def record_statistic(user, entries, score):
        print("Record Entries",entries)

        if not user.is_anonymous:
            protocol = ProtocolRecord(answer_user=user,score=score,
                                  test=entries[0]['question_id'].test)
        else:
            protocol = ProtocolRecord(answer_user=None, score=score,
                                      test=entries[0]['question_id'].test)


        protocol.save()

        answers_create = []

        for answer in entries:

            for item in answer['answer_id']:
                answer_record = UserAnswerRecord(protocol=protocol, question=answer['question_id'])
                answer_record.answer_id = item
                answers_create.append(answer_record)

            if len(answer['answer_text']) > 0:
                answer_record = UserAnswerRecord(protocol=protocol, question=answer['question_id'],
                                                 answer_text=answer['answer_text'])
                answers_create.append(answer_record)

        UserAnswerRecord.objects.bulk_create(answers_create)

        return protocol.pk
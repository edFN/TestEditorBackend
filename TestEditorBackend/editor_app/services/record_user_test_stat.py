from TestEditorBackend.editor_app.models import TestQuestionModel


class RecordStatisticService:
    @staticmethod
    def record_statistic(user, entries):
        question = entries[0]['question_id']
        pass #use bulk_create

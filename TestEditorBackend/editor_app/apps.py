from django.apps import AppConfig


class EditorAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'editor_app'

    def ready(self):
        try:
            from .models import TypeQuestionModel

            TypeQuestionModel.objects.get_or_create(name="Text")
            TypeQuestionModel.objects.get_or_create(name="ONE_VARIANT")
            TypeQuestionModel.objects.get_or_create(name="MULTIPLE_VARIANT")
        except:
            print("No table trying to add")
            


from TestEditorBackend.editor_app.models import MessageFinishedTest


def get_message_points(points):
    return MessageFinishedTest.objects.filter(points__gte=points)\
        .order_by('points').first().values()
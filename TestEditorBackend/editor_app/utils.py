from django.db.models import Q
from django.utils.encoding import force_str
from editor_app.models import MessageFinishedTest
from rest_framework.metadata import SimpleMetadata
from rest_framework.relations import HyperlinkedRelatedField, PrimaryKeyRelatedField, RelatedField, ManyRelatedField


def get_message_points(points, instance):
    print(points)
    item = MessageFinishedTest.objects.filter(Q(points__lte=points) & Q(test=instance))\
        .order_by('points').last()

    if item is None:
        return ""

    return item.text

class MyMetaData(SimpleMetadata):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            print('lookup', self.label_lookup)

        def get_field_info(self, field):

            field_info = super(MyMetaData, self).get_field_info(field)
            if isinstance(field, (HyperlinkedRelatedField, PrimaryKeyRelatedField, RelatedField, ManyRelatedField)):
                field_info['choices'] = [
                    {
                        'value': choice_value,
                        'display_name': force_str(choice_name, strings_only=True)
                    }
                    for choice_value, choice_name in field.get_choices().items()
                ]

            if isinstance(field, (ManyRelatedField,)):
                field_info['multiple'] = True
            return field_info


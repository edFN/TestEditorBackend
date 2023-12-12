from django.db import models

from authentication.models import User


class TypeTestModel(models.Model):
    name = models.CharField("Тип теста", max_length=100)

    def __str__(self):
        return self.name or ''


class HashTagsModel(models.Model):
    name = models.CharField("Название хэштега", max_length=200)

    def __str__(self):
        return self.name or ''

class TestModel(models.Model):
    author = models.ForeignKey(User, verbose_name='Автор', null=False, blank=False, on_delete=models.CASCADE)

    title = models.CharField("Название", max_length=256, null=True, blank=False)

    views = models.PositiveIntegerField(verbose_name="Просмотрено", default=0, null=False)

    description = models.TextField("Описание", null=True, blank=True)

    image = models.ImageField("Изображение", null=True, blank=True)

    is_private = models.BooleanField("Приватный", null=False, default=False)

    is_record_statistic = models.BooleanField("Записывать статистику", null=True, blank=True, default=False)

    is_different_msg = models.BooleanField("Сообщения в зависимости от баллов", null=True,blank=True, default=False)

    type = models.ForeignKey(to=TypeTestModel, verbose_name="Тип теста", null=True, on_delete=models.SET_NULL)

    hashtags = models.ManyToManyField(HashTagsModel, verbose_name="Хэштеги", null=True,blank=True)

    created_at = models.DateField("Создан", auto_now=True)


    def has_messages(self):
        return MessageFinishedTest.objects.filter(test=self).exists()


    def __str__(self):
        return self.title or ''


class MessageFinishedTest(models.Model):
    test = models.ForeignKey(TestModel, null=True, blank=True, related_name='message_finish_rel',
                             on_delete=models.CASCADE)
    text = models.TextField(null=True,blank=False)

    points = models.IntegerField(default=0)


class TypeQuestionModel(models.Model):
    name = models.CharField("Название поля", max_length=200, null=False, blank=False)

    def __str__(self):
        return self.name or ''


class TestQuestionModel(models.Model):
    test = models.ForeignKey(TestModel, null=True, blank=True, related_name='test_question_rel',
                             on_delete=models.CASCADE)
    question = models.TextField("Вопрос", max_length=256, null=True, blank=True)
    type = models.ForeignKey(TypeQuestionModel, null=True, blank=True, on_delete=models.SET_NULL)

    has_diff_point = models.BooleanField(default=False)

    def __str__(self):
        return self.question or ''


class TestAnswerModel(models.Model):
    question = models.ForeignKey(TestQuestionModel, null=True, related_name='question_answer_rel',
                                 blank=True, on_delete=models.CASCADE)
    answer_text = models.CharField("Ответ(текст)", null=True, blank=True, max_length=256)
    answer_image = models.ImageField("Ответ(изображение)", null=True, blank=True)

    answer_points = models.IntegerField("Баллы за ответ", default=1)

    is_right = models.BooleanField("Правильный ответ", default=False, null=False)

    def __str__(self):
        return f'{self.question}#{self.pk}'


class ProtocolRecord(models.Model):
    create_at = models.DateField(auto_now=True)
    answer_user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

class UserAnswerRecord(models.Model):
    protocol = models.ForeignKey(ProtocolRecord, null=True, blank=False, on_delete=models.CASCADE)
    question = models.ForeignKey(TestQuestionModel, null=False, blank=False, on_delete=models.CASCADE)
    answer_id = models.ForeignKey(TestAnswerModel, null=False, blank=True, on_delete=models.CASCADE)
    answer_text = models.CharField("Неправильный ответ в виде текста", null=True,blank=True,max_length=256)

    def __str__(self):
        return f'ответ пользователя {self.answer_user}'

# class AnswerModel(models.Model):
#     question = models.ForeignKey(TestQuestionModel, null=True, blank=True, on_delete=models.CASCADE)
#     image = models.ImageField("Изображение", null=True,bl)



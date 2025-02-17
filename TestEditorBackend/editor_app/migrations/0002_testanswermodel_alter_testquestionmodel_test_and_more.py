# Generated by Django 4.2.7 on 2023-11-26 08:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('editor_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestAnswerModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.CharField(blank=True, max_length=256, null=True, verbose_name='Ответ(текст)')),
                ('answer_image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Ответ(изображение)')),
                ('is_right', models.BooleanField(default=False, verbose_name='Правильный ответ')),
            ],
        ),
        migrations.AlterField(
            model_name='testquestionmodel',
            name='test',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='test_question_rel', to='editor_app.testmodel'),
        ),
        migrations.CreateModel(
            name='UserAnswerRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_id', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='editor_app.testanswermodel')),
                ('answer_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='editor_app.testquestionmodel')),
            ],
        ),
        migrations.AddField(
            model_name='testanswermodel',
            name='question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='question_answer_rel', to='editor_app.testquestionmodel'),
        ),
    ]

from django.contrib import admin

from .models import TypeTestModel, TestModel, TestQuestionModel, TypeQuestionModel, HashTagsModel


# Register your models here.

@admin.register(TypeTestModel)
class TypeTestAdmin(admin.ModelAdmin):
    pass


@admin.register(TestModel)
class TestAdmin(admin.ModelAdmin):
    pass


@admin.register(TypeQuestionModel)
class TypeQuestionAdmin(admin.ModelAdmin):
    pass

@admin.register(TestQuestionModel)
class TestQuestionAdmin(admin.ModelAdmin):
    pass

@admin.register(HashTagsModel)
class HashTagAdmin(admin.ModelAdmin):
    pass
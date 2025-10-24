from django.contrib import admin
from english.models import Student, Test, TestQuestion, TestQuestionVariant, Result

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'login', 'level', 'progress', 'results_count']
    
    def results_count(self, obj):
        return obj.result_set.count()
    results_count.short_description = 'Пройдено тестов'

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'questions_count']
    
    def questions_count(self, obj):
        return obj.testquestion_set.count()
    questions_count.short_description = 'Кол-во вопросов'

@admin.register(TestQuestion)
class TestQuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'answer', 'test', 'variants_count']
    
    def variants_count(self, obj):
        return obj.testquestionvariant_set.count()
    variants_count.short_description = 'Вариантов ответа'

@admin.register(TestQuestionVariant)
class TestQuestionVariantAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'is_corect', 'test_question']

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'test', 'score', 'date', 'student_level']
    
    def student_level(self, obj):
        return obj.student.level
    student_level.short_description = 'Уровень ученика'
from django.contrib import admin
from english.models import Student, Test, TestQuestion, TestQuestionVariant, Result
from general.models import UserProfile
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'login', 'level', 'progress', 'results_count', 'assigned_tutor_name']

    def results_count(self, obj):
        return obj.result_set.count()
    results_count.short_description = 'Пройдено тестов'

    def assigned_tutor_name(self, obj):
        return obj.tutor.userprofile.name if obj.tutor and hasattr(obj.tutor, 'userprofile') else "-"
    assigned_tutor_name.short_description = 'Тьютор'

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'questions_count']

    def questions_count(self, obj):
        return obj.questions.count()
    questions_count.short_description = 'Кол-во вопросов'

@admin.register(TestQuestion)
class TestQuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'test', 'variants_count']
    def variants_count(self, obj):
        return obj.variants.count()
    variants_count.short_description = 'Вариантов ответа'

@admin.register(TestQuestionVariant)
class TestQuestionVariantAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'is_correct', 'test_question']

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'test', 'score', 'date', 'student_level']
    
    def student_level(self, obj):
        return obj.student.level
    student_level.short_description = 'Уровень ученика'
    
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'type', 'created_at')
    list_filter = ('type',)
    search_fields = ('user__username', 'name')
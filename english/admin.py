from django.contrib import admin
from english.models import Student, Word, Test, Result, Lesson

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'login', 'level', 'progress', 'test_results_count']
    
    def test_results_count(self, obj):
        return obj.result_set.count()
    test_results_count.short_description = 'Пройдено тестов'

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ['id', 'word', 'translation', 'topic', 'used_in_lessons']
    
    def used_in_lessons(self, obj):
        return obj.lesson_set.count()
    used_in_lessons.short_description = 'Уроков с словом'

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'answer', 'words_count', 'lesson_topic']
    
    def words_count(self, obj):
        return obj.words.count()
    words_count.short_description = 'Кол-во слов'
    
    def lesson_topic(self, obj):
        if obj.lesson:
            return obj.lesson.ltopic
        return "Нет урока"
    lesson_topic.short_description = 'Тема урока'

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'test', 'score', 'date', 'student_level']
    
    def student_level(self, obj):
        return obj.student.level
    student_level.short_description = 'Уровень ученика'

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['id', 'ltopic', 'ltest', 'words_count', 'has_test']
    
    def words_count(self, obj):
        return obj.words.count()
    words_count.short_description = 'Кол-во слов'
    
    def has_test(self, obj):
        return "Да" if obj.test else "Нет"
    has_test.short_description = 'Есть тест'
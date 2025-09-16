from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets
from english.models import Student, Word, Test, Result, Lesson
from english.serializers import StudentSerializer, WordSerializer, TestSerializer, ResultSerializer, LessonSerializer

class StudentsViewset(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class WordsViewset(mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = Word.objects.all()
    serializer_class = WordSerializer

class TestsViewset(mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

class ResultsViewset(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer

class LessonsViewset(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
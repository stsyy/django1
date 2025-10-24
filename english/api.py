from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.parsers import MultiPartParser, FormParser
from english.models import Student, Test, TestQuestion, Result
from english.serializers import StudentSerializer, TestSerializer, TestQuestionSerializer, ResultSerializer

class StudentsViewset(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    parser_classes = (MultiPartParser, FormParser) 

class TestsViewset(mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

class TestQuestionsViewset(mixins.CreateModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.ListModelMixin,
                           GenericViewSet):
    queryset = TestQuestion.objects.all()
    serializer_class = TestQuestionSerializer

class ResultsViewset(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer


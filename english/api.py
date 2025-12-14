from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.parsers import MultiPartParser, FormParser
from english.models import Student, Test, TestQuestion, Result
from english.serializers import StudentSerializer, TestSerializer, TestQuestionSerializer, ResultSerializer
from rest_framework.decorators import action

from english.models import Student, Test, TestQuestion, TestQuestionVariant, Result, Tutor
from .serializers import StudentSerializer, TestQuestionSerializer, TestSerializer, ResultSerializer, TestQuestionVariantSerializer, TutorSerializer

class StudentsViewset(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    parser_classes = (MultiPartParser, FormParser)
    
class StudentsViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Student.objects.all().order_by("-id")
    serializer_class = StudentSerializer

  #  @action(detail=False, url_path="create-custom", methods=['POST'], permission_classes=[CanSeePage1Permission])
    def create_custom(self, request, *args, **kwargs):
        student = Student.objects.create()
        return Response({
            "success": True
        })

 #   @action(detail=False, url_path="create-custom-group", methods=['POST'], permission_classes=[SecondFactorPermission])
    def create_custom_group(self, request, *args, **kwargs):
        student = Student.objects.create()
        return Response({
            "success": True
        })

     

class TestsViewSet(mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

class TestQuestionsViewSet(mixins.CreateModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.ListModelMixin,
                           GenericViewSet):
    queryset = TestQuestion.objects.all()
    serializer_class = TestQuestionSerializer

class ResultsViewSet(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer


from django.shortcuts import render
from django.http import HttpResponse
from english.models import Student
from django.views.generic import TemplateView
from typing import Any 
from rest_framework import views 
from rest_framework import viewsets
from english.models import TestQuestion
from .serializers import StudentSerializer, TestQuestionSerializer
from django.contrib.auth import logout # Импортируем функцию logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST']) # Обычно используют POST для действий, меняющих состояние (выход)
@permission_classes([]) # Разрешаем всем (авторизованным)
def logout_view(request):
    """Сбрасывает сессию пользователя."""
    if request.user.is_authenticated:
        logout(request)
        return Response({'detail': 'Успешный выход из системы.'}, status=status.HTTP_200_OK)
    else:
        return Response({'detail': 'Вы не авторизованы.'}, status=status.HTTP_401_UNAUTHORIZED)

# Create your views here.
#class ShowStudentsView(TemplateView):
 #   template_name="students/show_students.html"
  #  def get_context_data(self, **kwargs) -> dict[str, Any]:
   #     context = super().get_context_data(**kwargs)
    #    context["students"] = Student.objects.all()
     #   return context
     
     #из методчики
class StudentsViewset(
viewsets.ModelViewSet
):
    #queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_queryset(self):

        user = self.request.user

        if user.is_superuser:
            return Student.objects.all()
        else:

            return Student.objects.filter(user=user)
        

class TestQuestionViewSet(viewsets.ModelViewSet):
    serializer_class = TestQuestionSerializer
    
    def get_queryset(self):
        user = self.request.user
        
        # 1. Проверяем, является ли пользователь администратором 
        if user.is_superuser:
            # Администраторы видят все вопросы
            return TestQuestion.objects.all()
        else:
            # Обычные пользователи (студенты) не должны видеть этот список
            return TestQuestion.objects.none()
from django.shortcuts import render
from django.http import HttpResponse
from english.models import Student
from django.views.generic import TemplateView
from typing import Any 

# Create your views here.
#class ShowStudentsView(TemplateView):
 #   template_name="students/show_students.html"
  #  def get_context_data(self, **kwargs) -> dict[str, Any]:
   #     context = super().get_context_data(**kwargs)
    #    context["students"] = Student.objects.all()
     #   return context
     
     #из методчики
class StudentsViewset(
    # ...
):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        
        # фильтруем по текущему юзеру
        qs = qs.filter(user=self.request.user)

        return qs
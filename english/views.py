# english/views.py
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.db.models import Prefetch

from english.models import Student, Test, TestQuestion, TestQuestionVariant, Result, Tutor

# Create your views here.
def students_list(request):
    return HttpResponse("{ title: 123 }")

class StudentsList(View):
    def get(self, *args, **kwargs):
        return HttpResponse("Новый метод")
    

class StudentsListTemplate(TemplateView):
    template_name = "students/list.html"

    def get_context_data(self, **kwargs):
        groups = Group.objects.prefetch_related(
            Prefetch("students", queryset=Student.objects.filter(age__gte=20), to_attr="old_students")
        ).all()
        
        result = []
        for group in groups:
            result.append({
                "group": group,
                "students": group.old_students
            })

        return {
            'items': result,
            'user': self.request.user,
            'userprofile': self.request.user.userprofile,
        }

from django.shortcuts import render
from django.http import HttpResponse
from english.models import Student
from django.views import View

# Create your views here.
class ShowStudentsView(View):
    def get(request, *args, **kwargs):
    #return HttpResponse("Привет!")
        students=Student.objects.all()
    
        result = ""
    
        for s in students:
            result += s.name + "<br>"
        
        return HttpResponse(result)    
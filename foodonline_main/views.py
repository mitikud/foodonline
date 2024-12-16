from django.shortcuts import render
from django.http import HttpResponse


# def home(request):
#     return HttpResponse('Hello world')
def home(request):
    return render(request, 'home.html')



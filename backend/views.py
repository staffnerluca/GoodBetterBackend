from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def get_current_course_lesson(request):
    return JsonResponse({"basicMorality": "10"})
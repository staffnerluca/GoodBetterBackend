from django.urls import path
from .views import get_current_course_lesson

urlpatterns = [
    path('get_current_course_lesson/', get_current_course_lesson),
]
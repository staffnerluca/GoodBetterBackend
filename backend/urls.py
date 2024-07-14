from django.urls import path
from .views import get_current_course_lesson, login, register

urlpatterns = [
    path('get_current_course_lesson/', get_current_course_lesson),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
]
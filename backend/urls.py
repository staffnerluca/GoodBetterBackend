from django.urls import path
from .views import get_current_course_lesson, get_eating_meat_days, login_view, register

urlpatterns = [
    path('get_current_course_lesson/', get_current_course_lesson),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('get_meat_days/', get_eating_meat_days, name='get_meat_days')
]
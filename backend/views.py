from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import F, Q, Sum # F: access field values directely; Q: advanced conditions
from django.db.models.functions import Abs
from .models import UserProfile, CustomUser, Days, Course, CourseQuestion
from .serializers import CourseQuestionSerializer, CourseSerializer, UserProfileSerializer, DaysSerializer
import random
import json
import datetime
import os
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from django.core import serializers
from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.core.files.base import ContentFile


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email_address=email, password=password)
        if user is not None:
            login(request, user)
            return Response({'message': 'Login succeseful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid login information'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'Methode not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    return Response({"message":"success"}, status = status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_current_course_lesson(request):
    return Response({"basicMorality": "10"})
 

# Creating stuff
def create_course():
    pass


@api_view(['POST'])
@permission_classes([AllowAny])
def create_user_profile(request):
    data = request.data
    try:
        user_profile = UserProfile.objects.create(
            first_name=data['first_name'],
            second_name=data['second_name'],
            username=data['username'],
            country=data['country'],
            birth_date=data['birth_date'],
            wants_to_become_vegetarian=data['wants_to_become_vegetarian']
        )
        return Response({"message": "Created user"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': f"Error when creating UserProfile: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


def get_eating_meat_days(username):
    meat_days_dic = {
        "Mo": 0,
        "Tu": 0,
        "We": 0,
        "Th": 0,
        "Fr": 0,
        "Sa": 0,
        "Su": 0
    }
    user = get_object_or_404(UserProfile, username = username)
    user_meat_days = user.meat_days.split(",")
    for day in user_meat_days:
        meat_days_dic[day] = 1
    return meat_days_dic


def get_calendar(userProfile):
    days = Days.objects.filter(user=userProfile)
    days_data = {}
    for day in days:
        days_data[day.date] = {
            "date" : day.date,
            "vegetarian_status" : day.vegetarian_status
        }
    return list(days_data.values())


def get_calendar_test(request):
    username = request.GET.get('username')
    userProfile = get_object_or_404(UserProfile, username = username)
    days = Days.objects.filter(user=userProfile)
    days_data = [{
        "date": day.date,
        "vegetarian_status": day.vegetarian_status
    } for day in days]
    return Response(days_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_data_for_vegetarian_streak_page(request):
    print("start getting data")
    username = request.GET.get("username")
    if not username:
        return Response({"Error": "No username given"}, status=status.HTTP_400_BAD_REQUEST)
    userProf = UserProfile.objects.get(username=username)
    if(not userProf.wants_to_become_vegetarian):
        return Response({"Vegetarian": "False"}, status=status.HTTP_200_OK)
    #check how to handle duplicates later 
    data = {
        "meat_days": get_eating_meat_days(username),
        "not_eating_meat_streak": userProf.not_eating_meat_streak,
        "calendar": get_calendar(userProf)        
        }
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_questions_by_course(request, course_id):
    try:
        questions = CourseQuestion.objects.filter(course=course_id)
        if not questions.exists():
            return Response({'error': 'No questions found for this course'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CourseQuestionSerializer(questions, many=True)
        
        questions_dict = {question['id']: question for question in serializer.data}
        
        return Response(questions_dict)
    except CourseQuestion.DoesNotExist:
        return Response({'error': 'Course does not exist'}, status=status.HTTP_404_NOT_FOUND)
    

# can only be created once. After that the username needs to be changed
@api_view(['GET'])
@permission_classes([AllowAny])
def create_test_users(request):
    try:
        for i in range(10):
            email = f"new_user{i}@example.com"
            user = CustomUser.objects.create_user(username=email, email_address=email, password='password')

            UserProfile.objects.create(
                user=user,
                first_name=f"FirstName{i}",
                second_name=f"SecondName{i}",
                username=f"username{i}",
                country="US",
                birth_date=timezone.now().date() - timedelta(days=i * 365),
                isAdmin=bool(i % 2),
                wants_to_become_vegetarian=bool(i % 3),
                not_eating_meat_streak=i * 5,
                course_streak=i * 2,
                joined_at=timezone.now().date() - timedelta(days=i * 30),
                total_time_on_the_app_in_minutes=i * 100,
                meat_days="Mon,Fri" if i % 2 == 0 else "Tu,Th"
            )

        print("10 example datasets created.")
        return Response({"message": "Created 10 test users"}, status=status.HTTP_201_CREATED)
    except Exception as error:
        return Response({"message":"Users where already created."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_test_days(request):
    for i in range(10):
        user_profile = UserProfile.objects.get(username="username1")
        with transaction.atomic():
            for i in range(30):
                day = timezone.now().date() - timezone.timedelta(days = i)
                vegetarian_status = random.choice(["v", "m", "f"])
                Days.objects.create(
                    user = user_profile,
                    date = day,
                    vegetarian_status = vegetarian_status
                )
    return Response({"message": "Created days"}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_users(request):
    profiles = UserProfile.objects.all()
    profiles_data = serializers.serialize('json', profiles)
    return Response(profiles_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def change_eating_meat_days(request):
    username = request.data.get('username'),
    user = UserProfile.objects.get(username = username)
    user.meat_days = request.data.get("meat_days")
    return Response({"message": "changed succesefully"}, status=status.HTTP_200_OK)


def parse_free_days(user):
    meat_days = user.meat_days
    meat_days = meat_days.split(",")
    days = {}
    for i in range(7):
        day = datetime.datetime.now() + datetime.timedelta(days=i - datetime.datetime.now().weekday())
        day = day.strftime("%a")
        if day in meat_days:
            days[day] = True
        else:
            days[day] = False
    print(days)
    return days 


@api_view(['GET'])
@permission_classes([AllowAny])
def is_free_day(request):
    username = request.GET.get("username")
    user_profile = get_object_or_404(UserProfile, username=username)
    meat_days = parse_free_days(user_profile)
    print(meat_days)
    weekday_num = datetime.datetime.now() + datetime.timedelta(days=datetime.datetime.now().weekday())
    weekday = weekday_num.strftime("%a")
    if meat_days[weekday]:
        return Response({"freeDay" : True}, status=status.HTTP_200_OK)
    else:
        return Response({"freeDay" : False}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def post_did_user_eat_meat(request):
    data = request.data
    username = data["username"]
    vegetarian_status = data["vegetarian_status"]
    user = get_object_or_404(UserProfile, username=username)
    today = datetime.datetime.today()
    current_date = Days.objects.filter(user = user, date = today).first()
    if current_date:
        current_date.vegetarian_status = vegetarian_status
        current_date.save()
    else:
        day = Days.objects.create(
            user = user,
            date = today,
            vegetarian_status = vegetarian_status
        )
    return Response({"message": "success"}, status=status.HTTP_200_OK)
    

@api_view(['GET'])
@permission_classes([AllowAny])
def get_course(request, course_id):
    course = Course.objects.all()
    course_data = serializers.serialize("json", course)
    return Response(course_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_courses(request):
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_username_from_mail(request):
    mail = request.GET.get("mail")
    user = CustomUser.objects.filter(email_address = mail).first()
    user_profile = UserProfile.objects.filter(user = user).first()
    return Response({"username": user_profile.username}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def create_example_course_questions(request):
    with transaction.atomic():
        what_believe_image_path = "what_believe.png"
        try:
            with open(what_believe_image_path, "rb") as img:
                what_believe_content = img.read()
        except FileNotFoundError:
            return Response({"message":settings.MEDIA_ROOT}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        what_believe_file = ContentFile(what_believe_content, 'what_believe.png')
        course = Course.objects.create(
            name="What I believe and what I should believe",
            goal="Teaches basics of morality and starts to ask relevant questions",
            image="http://127.0.0.1:8000/api/media/what_believe.png"
        )
        
        # Create questions
        question_1 = CourseQuestion.objects.create(
            name="Eat Meat?",
            content="Do you eat meat?",
            image="",
            course=course,
            is_first=True,
            is_boolean=True,
            options=""
        )

        question_2 = CourseQuestion.objects.create(
            name="Factory-Farmed Meat?",
            content="Do you eat factory-farmed meat?",
            image="",
            course=course,
            is_boolean=True,
            options=""
        )
        
        question_3 = CourseQuestion.objects.create(
            name="Spend on Meat?",
            content="On average, how much do you spend on meat-eating every week?",
            image="",
            course=course,
            is_boolean=False,
            options="int"
        )
        
        question_4 = CourseQuestion.objects.create(
            name="Meat Proportions?",
            content="What proportion of meat you eat is factory-farmed, and what proportion of meat you eat is non-factory farmed?",
            image="",
            course=course,
            is_boolean=False,
            options="percent"
        )
        
        question_5 = CourseQuestion.objects.create(
            name="Types of Meat?",
            content="In proportion, what types of meat do you eat? (beef, chicken, pork, fish, …)",
            image="",
            course=course,
            is_boolean=False,
            options="percent: beef, chicken, pork, fish"
        )
        
        question_6 = CourseQuestion.objects.create(
            name="Slavery Wrong?",
            content="If you have to bet, would you bet that slavery is, in fact, morally wrong?",
            image="",
            course=course,
            is_boolean=True,
            options=""
        )
        
        question_7 = CourseQuestion.objects.create(
            name="Factory-Farmed Meat Wrong?",
            content="If you have to bet, would you bet that eating factory-farmed meat is, in fact, morally wrong?",
            image="",
            course=course,
            is_boolean=True,
            options=""
        )
        
        question_8_yes = CourseQuestion.objects.create(
            name="Why Factory-Farmed Meat?",
            content="Then, why do you still eat factory-farmed meat?",
            image="",
            course=course,
            is_boolean=False,
            options=""
        )
        
        question_8_no = CourseQuestion.objects.create(
            name="Why Permissible?",
            content="Why is eating factory-farmed meat morally permissible?",
            image="",
            course=course,
            is_boolean=False,
            options=""
        )
        
        # Link questions based on the provided flow
        question_1.next_question_if_true = question_2
        question_1.next_question_if_false = question_2

        question_2.next_question_if_true = question_3
        question_2.next_question_if_false = question_3

        question_3.next_question_if_true = question_4
        question_3.next_question_if_false = question_4

        question_4.next_question_if_true = question_5
        question_4.next_question_if_false = question_5

        question_5.next_question_if_true = question_6
        question_5.next_question_if_false = question_6

        question_6.next_question_if_true = question_7
        question_6.next_question_if_false = question_7

        question_7.next_question_if_true = question_8_yes
        question_7.next_question_if_false = question_8_no

        # Save all changes to the database
        question_1.save()
        question_2.save()
        question_3.save()
        question_4.save()
        question_5.save()
        question_6.save()
        question_7.save()
        question_8_yes.save()
        question_8_no.save()

    return Response({"message": "Created course questions successfully"}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_days(request):
    days = Days.objects.all()
    days_json = DaysSerializer(days, many=True)
    return Response(days_json.data, status=status.HTTP_200_OK)
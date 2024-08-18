from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import F, Q, Sum # F: access field values directely; Q: advanced conditions
from django.db.models.functions import Abs
from .models import UserProfile, CustomUser, Days
import random
import json
from datetime import timedelta
from django.utils import timezone
from django.core import serializers
from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status


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


@api_view(['GET'])
@permission_classes([AllowAny])
def get_current_course_lesson(request):
    return Response({"basicMorality": "10"})


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        username = data.get('username')
        print(email)
        print(password)
        print(username)
        User = get_user_model()
        try:
            user = User.objects.create_user(email_address=email, username=username, password=password)
            login(request)
            return Response({'message': 'Registration successful'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
 

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



# can only be created once. After that the username needs to be changed
@api_view(['POST'])
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
                meat_days="Mo,Fr" if i % 2 == 0 else "Tu,Th"
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


@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_days(request):
    days = Days.objects.all()
    days_json = serializers.serialize('json', days)
    return Response(days_json, status=status.HTTP_200_OK)
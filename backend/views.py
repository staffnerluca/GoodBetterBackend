from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import F, Q, Sum # F: access field values directely; Q: advanced conditions
from django.db.models.functions import Abs
from .models import UserProfile, CustomUser
import random
import json
from datetime import timedelta
from django.utils import timezone


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        print(email)
        print(password)
        user = authenticate(request, email_address=email, password=password)
        if user is not None:
            login(request, user)
            print("I am here")
            return JsonResponse({'message': 'Login succeseful'})
        else:
            return JsonResponse({'error': 'Invalid login information'}, status=400)
    return JsonResponse({'error': 'Methode not allowed'}, status=405)


#course logic for the user
@csrf_exempt
def get_current_course_lesson(request):
    return JsonResponse({"basicMorality": "10"})


@csrf_exempt  # Disable CSRF for external requests (ensure security measures are in place)
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        username = data.get('username')
        print(email)
        print(password)
        print(username)
        # Create a new user
        User = get_user_model()
        try:
            user = User.objects.create_user(email_address=email, username=username, password=password)
            login(request)
            return JsonResponse({'message': 'Registration successful'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
 

# Creating stuff
def create_course():
    pass


@csrf_exempt
def create_user_profile(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            fn = data['first_name']
            sn = data['second_name']
            un = data['username']
            c = data['country']
            bd = data['birth_date']
            ci = data['categorical_imperative']
            ve = data['virtue_ethics']
            ar = data['animal_rights']
            wbv = data['wants_to_become_vegetarian']
            dnpg = data['donations_per_week_goal']

            user_profile = UserProfile()
            user_profile.first_name = fn
            user_profile.second_name = sn
            user_profile.username = un
            user_profile.country = c
            user_profile.brit_date = bd
            user_profile.categorical_imperative = ci
            user_profile.virtue_ethics = ve
            user_profile.animal_rights = ar
            user_profile.wants_to_become_vegetarian = wbv
            user_profile.donations_per_week_goal = dnpg
        except Exception as e:
            print("Error when creating UserProfile: "+e)


@csrf_exempt
def get_eating_meat_days(request, username):
    meat_days_dic = {
        "Mo": 0,
        "Di": 0,
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
    return JsonResponse({"meat_days": meat_days_dic})


# can only be created once. After that the username needs to be changed
def create_test_users(request):
    print("Start creating test users")
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
    return JsonResponse({"Status": "Created"})

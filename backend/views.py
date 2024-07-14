from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import UserProfile


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login succeseful'})
        else:
            return JsonResponse({'error': 'Invalid login information'}, status=400)

    # Falls GET- oder anderer Request-Methode
    return JsonResponse({'error': 'Methode not allowed'}, status=405)


#course logic for the user
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
            user = User.objects.create_user(email=email, username=username, password=password)
            login(request, user)
            return JsonResponse({'message': 'Registration successful'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def check_login(request):
    pass
 

# Creating stuff
def register_user(request):
    pass


def create_course():
    pass


def create_good_thing():
    pass

# Update
def update_user_moral_alignment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ci = data["categorical_imperative"]
            ut = data["utilitarian"]
            ve = data["virute_ethics"]
            ar = data["animal_rights"]
            lo = data["longtermism"]
            user_id = data["user_id"]
            user = get_object_or_404(UserProfile, id=user_id)
            user.categorical_imperative = ci
            user.utilitarian = ut
            user.virute_ethics = ve
            user.animal_rights = ar
            user.longtermism =  lo
            user.save()
        except json.JSONDecodeError:
            return JsonResponse({"error": "Inavalid JSOn"}, status = 400)
        
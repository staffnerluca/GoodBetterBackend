from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import F, Q, Sum # F: access field values directely; Q: advanced conditions
from django.db.models.functions import Abs
import json
from .models import UserProfile, EthicalTypes, GoodThing



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


def create_good_thing():
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
            user.categorical_imperative += ci
            user.utilitarian += ut
            user.virtue_ethics += ve
            user.animal_rights += ar
            user.longtermism += lo
            user.save()
        except json.JSONDecodeError:
            return JsonResponse({"error": "Inavalid JSOn"}, status = 400)


# GET stuff
def get_user_ethical_type(user_profile):
    ethical_type = EthicalTypes.objects.annotate(
        dif = (
            Abs(F('categorical_imperative') - user_profile.categoric_imperative) +
            Abs(F('utilitarian') - user_profile.utilitarian) +
            Abs(F('virtue_ethics') - user_profile.virtue_ethics) +
            Abs(F('animal_rights') - user_profile.animal_rights) +
            Abs(F('longtermism') - user_profile.longtermism)
        )
    ).order_by('dif')
    return ethical_type.first()


def get_good_things_of_the_day(request):
    id = request['user_id']
    user = UserProfile.objects.get(user_id = id)
    user_ethic_type = get_user_ethical_type(user)
    if not user_ethic_type:
        return JsonResponse({"error": "No ethical type found"})
    relevant_donations = GoodThing.objects.filter(relevnat_for=user_ethic_type, thing_type = "donation")
    relevant_other_good_thing = GoodThing.objects.filter(relevant)


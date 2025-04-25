from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from datetime import datetime
import logging
import json
from .models import CarMake, CarModel

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Function to initialize some car makes if none exist
def initiate():
    # Create some default car makes if none exist
    CarMake.objects.create(name="Toyota", description="Japanese car maker")
    CarMake.objects.create(name="Honda", description="Japanese car manufacturer")
    CarMake.objects.create(name="Ford", description="American car manufacturer")
    logger.info("Car makes initialized.")

# Get cars function
def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)
    if(count == 0):
        initiate()  # Call initiate to create car makes if the count is 0
    
    # Fetch car models with the related car make data
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    
    return JsonResponse({"CarModels": cars})

# Create a `login_user` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    
    # Try to authenticate the user
    user = authenticate(username=username, password=password)
    response_data = {"userName": username}
    
    if user is not None:
        # If user is valid, login the user
        login(request, user)
        response_data = {"userName": username, "status": "Authenticated"}
    
    return JsonResponse(response_data)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    response_data = {"userName": ""}
    return JsonResponse(response_data)

# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data['userName']
        password = data['password']
        first_name = data['firstName']
        last_name = data['lastName']
        email = data['email']

        # Check if username already exists
        username_exist = False
        try:
            User.objects.get(username=username)
            username_exist = True
        except User.DoesNotExist:
            logger.debug(f"{username} is a new user")

        if not username_exist:
            # Create new user
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            # Log the user in
            login(request, user)
            return JsonResponse({"userName": username, "status": "Authenticated"})
        else:
            return JsonResponse({"userName": username, "error": "Already Registered"})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)

# You can add more views for other actions such as adding reviews, getting reviews, etc.

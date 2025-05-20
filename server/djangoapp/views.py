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

# Function to initiate the database with sample data
def initiate():
    # Sample data to populate CarMake and CarModel
    car_make = CarMake.objects.create(name="Toyota", description="Japanese automobile manufacturer", website="https://www.toyota.com")
    car_make2 = CarMake.objects.create(name="Honda", description="Japanese automobile manufacturer", website="https://www.honda.com")
    
    # Populating CarModel for Toyota
    try:
        car_model = CarModel.objects.create(car_make=car_make, name="Corolla", type="SEDAN", year=2023, dealer_id=1)
        logger.info(f"Created car model {car_model}")
    except Exception as e:
        logger.error(f"Error creating Toyota model: {e}")
    
    car_model2 = CarModel.objects.create(car_make=car_make, name="Camry", type="SEDAN", year=2023, dealer_id=2)
    logger.info(f"Created car model {car_model2}")

    # Populating CarModel for Honda
    car_model3 = CarModel.objects.create(car_make=car_make2, name="Civic", type="SEDAN", year=2022, dealer_id=3)
    logger.info(f"Created car model {car_model3}")
    
    car_model4 = CarModel.objects.create(car_make=car_make2, name="Accord", type="SEDAN", year=2023, dealer_id=4)
    logger.info(f"Created car model {car_model4}")

# Create your views here.

# Create a `login_user` view to handle sign in request
@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)

# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    context = {}

    if request.method == "POST":
        data = json.loads(request.body)
        username = data['userName']
        password = data['password']
        first_name = data['firstName']
        last_name = data['lastName']
        email = data['email']

        username_exist = False
        try:
            User.objects.get(username=username)
            username_exist = True
        except User.DoesNotExist:
            logger.debug(f"{username} is a new user")

        if not username_exist:
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            login(request, user)
            return JsonResponse({"userName": username, "status": "Authenticated"})
        else:
            return JsonResponse({"userName": username, "error": "Already Registered"})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)

# Create a method to get the list of cars
def get_cars(request):
    count = CarMake.objects.filter().count()
    if(count == 0):
        initiate()

    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    
    return JsonResponse({"CarModels": cars})

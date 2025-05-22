from django.shortcuts import render, redirect, get_object_or_404  
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from datetime import datetime
import logging
import json
from .restapis import get_request, analyze_review_sentiments, post_review
from .models import CarMake, CarModel

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Function to initiate the database with sample data
def initiate():
    car_make = CarMake.objects.create(name="Toyota", description="Japanese automobile manufacturer", website="https://www.toyota.com")
    car_make2 = CarMake.objects.create(name="Honda", description="Japanese automobile manufacturer", website="https://www.honda.com")

    try:
        car_model = CarModel.objects.create(car_make=car_make, name="Corolla", type="SEDAN", year=2023, dealer_id=1)
        logger.info(f"Created car model {car_model}")
    except Exception as e:
        logger.error(f"Error creating Toyota model: {e}")

    car_model2 = CarModel.objects.create(car_make=car_make, name="Camry", type="SEDAN", year=2023, dealer_id=2)
    logger.info(f"Created car model {car_model2}")

    car_model3 = CarModel.objects.create(car_make=car_make2, name="Civic", type="SEDAN", year=2022, dealer_id=3)
    logger.info(f"Created car model {car_model3}")
    
    car_model4 = CarModel.objects.create(car_make=car_make2, name="Accord", type="SEDAN", year=2023, dealer_id=4)
    logger.info(f"Created car model {car_model4}")

# User authentication views
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

def logout_request(request):
    logout(request)
    return JsonResponse({"userName": ""})

@csrf_exempt
def registration(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data['userName']
        password = data['password']
        first_name = data['firstName']
        last_name = data['lastName']
        email = data['email']

        try:
            User.objects.get(username=username)
            return JsonResponse({"userName": username, "error": "Already Registered"})
        except User.DoesNotExist:
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
        return JsonResponse({"error": "Invalid request method"}, status=400)

# Car-related views
def get_cars(request):
    if CarMake.objects.count() == 0:
        initiate()

    car_models = CarModel.objects.select_related('car_make')
    cars = [{
        "CarModel": cm.name,
        "CarMake": cm.car_make.name,
        "Type": cm.type,
        "Year": cm.year,
        "DealerId": cm.dealer_id
    } for cm in car_models]
    
    return JsonResponse({"CarModels": cars})

# Dealer-related views
#Update the `get_dealerships` render list of dealerships all by default, particular state if state is passed
def get_dealerships(request, state="All"):
    if(state == "All"):
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/"+state
    dealerships = get_request(endpoint)
    return JsonResponse({"status":200,"dealers":dealerships})

def get_dealer_details(request, dealer_id):
    if(dealer_id):
        endpoint = "/fetchDealer/"+str(dealer_id)
        dealership = get_request(endpoint)
        return JsonResponse({"status":200,"dealer":dealership})
    else:
        return JsonResponse({"status":400,"message":"Bad Request"})

# ✅ NEW: Get dealer reviews with sentiment
def get_dealer_reviews(request, dealer_id):
    # if dealer id has been provided
    if(dealer_id):
        endpoint = "/fetchReviews/dealer/"+str(dealer_id)
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            print(response)
            review_detail['sentiment'] = response['sentiment']
        return JsonResponse({"status":200,"reviews":reviews})
    else:
        return JsonResponse({"status":400,"message":"Bad Request"})

@csrf_exempt
def add_review(request):
    if(request.user.is_anonymous == False):
        data = json.loads(request.body)
        try:
            response = post_review(data)
            return JsonResponse({"status":200})
        except:
            return JsonResponse({"status":401,"message":"Error in posting review"})
    else:
        return JsonResponse({"status":403,"message":"Unauthorized"})
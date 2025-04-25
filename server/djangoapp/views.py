from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

# Create a `login_user` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to authenticate the user
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, login the user
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
            # Check if username already exists
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

# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
# def get_dealerships(request):
#     ...

# Create a `get_dealer_reviews` view to render the reviews of a dealer
# def get_dealer_reviews(request, dealer_id):
#     ...

# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
#     ...

# Create an `add_review` view to submit a review
# def add_review(request):
#     ...

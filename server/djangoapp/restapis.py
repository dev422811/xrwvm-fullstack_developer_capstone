# Imports
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Environment config
backend_url = os.getenv('backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv('sentiment_analyzer_url', default="http://localhost:5050/")

# Function to make GET requests to the backend
def get_request(endpoint, **kwargs):
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params += f"{key}={value}&"
    request_url = backend_url + endpoint
    if params:
        request_url += "?" + params

    print("GET from {}".format(request_url))
    try:
        response = requests.get(request_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as err:
        print(f"Request error: {err}")
        return []

# Function to analyze review sentiments using sentiment analyzer microservice
def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url + "analyze/" + text
    print(f"Analyzing sentiment for: {text}")
    try:
        response = requests.get(request_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as err:
        print(f"Sentiment analysis error: {err}")
        return {"sentiment": "neutral"}  # fallback

# ✅ Function to submit a review to the backend
def post_review(data_dict):
    request_url = backend_url + "/insert_review"
    try:
        response = requests.post(request_url, json=data_dict)
        response.raise_for_status()
        print("Review submission response:", response.json())
        return response.json()
    except requests.exceptions.RequestException as err:
        print(f"Post review error: {err}")
        return {"status": "error", "message": "Network exception occurred"}

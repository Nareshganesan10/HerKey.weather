import json
import httpx
from django.shortcuts import render, redirect
from django.views.decorators import csrf
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from weather.models import CityModel, CustomUser, SearchModel


def home(request):
    city_list = CityModel.objects.all()
    if request.method == 'GET':
        return render(request, "home.html", {"city_list": city_list})
    elif request.method == "POST":
        # Initialize an HTTP client
        client = httpx.Client()

        # Extract the city name from the form submission
        city = request.POST['City']

        # If the city is 'my_city', retrieve the user's predefined city
        if city == 'my_city':
            city = request.user.user_city
        
        # Create a record of the searched location
        location_searched = SearchModel.objects.create(location_searched=city, username=str(request.user))
        location_searched.save()

        # Prepare the URL for the weather API request
        url = "https://api.weatherapi.com/v1/current.json?key=653feb430778453ab6d60823231406&q="+ str(city) + "&aqi=yes"

        # Make an API request to retrieve weather data
        api_request = client.get(url)

        # Check if the API request returned an error status code
        if api_request.status_code == 400:
            return render(request, "home.html", {"city_list": city_list, "status_code":400})
        
        try:
            # Parse the API response content as JSON
            api = json.loads(api_request.content)
        except Exception as e:
            api = "error"
        
        # Render the weather data along with city list and user information
        return render(request, "home.html", { "api": api, "city_list": city_list, "user": request.user})
    return Response("Retunedn home")



@api_view(['GET', 'POST'])
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate user with provided username and password
        user = authenticate(username=username, password=password)
                
        if user is not None:
            # If authentication is successful, log the user in and manage session variables
            login(request, user)
            request.session['user_id'] = user.id
            request.session['is_logged_in'] = True
            messages.success(request, "Logged in")
            return redirect('home')  # Redirect to the 'home' view
        else:
            messages.success(request, "Incorrect username or password")
            return redirect('signin')  # Redirect back to the sign-in page with a message
        
    # Handle GET request by rendering the sign-in page
    return render(request, "signin.html", {})


@api_view(['POST'])
@ensure_csrf_cookie
def signup(request):
    """
    This view function allows users to sign up for an account.
    """
    if request.method == 'POST':
        city = request.POST.get('city')
        mail = request.POST.get('mail')
        password = request.POST.get('password')
        retype_password = request.POST.get('retype_password')
        username = request.POST.get('username')

        # Check if provided passwords match
        if password == retype_password:
            # Check if the email already exists
            if CustomUser.objects.filter(email=mail).exists():
                messages.success(request, "Email already exists. Please try with another email.")
                return redirect('signup')
            else:
                # Create a new user account
                user = CustomUser.objects.create(username=username, password=password, email=mail, user_city=city)
                user.save()
                messages.success(request, "Account successfully created")

                # Authenticate and log in the user
                new_user = authenticate(username=username, password=password)
                if new_user is not None:
                    login(request, new_user)
                    messages.success(request, "Logged in")
                    return redirect('home')
                return redirect('signup')  # Redirect if authentication fails

        else:
            messages.success(request, "Password and Password confirmation did not match")
            return redirect('signup')

    # Render the signup form for GET requests
    return render(request, "signup.html", {})



@ensure_csrf_cookie
def signout(request):
    logout(request)  # Terminate the user's session
    messages.success(request, "Logged out")
    return redirect('signin')  # Redirect to the sign-in page


def authenticate(username, password):
    """
    Custom authentication function to authenticate a user.
    This function attempts to authenticate a user by checking if a `CustomUser` instance with the provided
    username and password exists in the database.
    """
    if CustomUser.objects.filter(username=username, password=password).exists():
        user = CustomUser.objects.get(username=username)
    else:
        user = None
    return user



def about_me(request):
    return render(request, "aboutme.html", {})

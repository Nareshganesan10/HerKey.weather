from django.shortcuts import render, redirect
import json
import requests
from django.views.decorators import csrf
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from weather.models import CityModel, CustomUser

def home(request):
    city_list = CityModel.objects.all()
    if request.method == 'GET':
        return render(request, "home.html", {"city_list": city_list})
    elif request.method == "POST":
        city = request.POST['City']
        api_request = requests.get("http://api.weatherapi.com/v1/current.json?key=653feb430778453ab6d60823231406&q="+ str(city) + "&aqi=yes")
        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "error"
    return render(request, "home.html", { "api": api, "city_list": city_list, "user": request.user})


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@ensure_csrf_cookie
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username, password)
        print(user)
        if user is not None:
            login(request, user)
            request.session['user_id'] = user.id
            request.session['is_logged_in'] = True
            messages.success(request,"Logged in")
            return redirect('home')
        else:
            messages.success(request, "incorrect username or password")
            return redirect('signin')
    return render(request, "signin.html", {})



@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@ensure_csrf_cookie
def signup(request):
    if request.method == 'POST':
        address = request.POST.get('Address')
        mail = request.POST.get('mail')
        password = request.POST.get('password')
        retype_password=request.POST.get('retype_password')
        username = request.POST.get('username')
        if password ==  retype_password:
            if CustomUser.objects.filter(email=mail).exists():
                messages.success(request, "request,Email already exists, Please try with another email")
                return redirect('signup')
            else:
                user =  CustomUser.objects.create(username=username, password=password, email=mail, user_address=address)
                user.save()
                messages.success(request, "Account succesfully created")
                new_user = authenticate(username, password)
                if new_user is not None:
                    login(request, new_user)
                    messages.success(request,"Logged in")
                    return redirect('home')
                return redirect('signup')
        else:
            messages.success(request,"password and Password confirmation did not match")
            return redirect('signup')
    return render(request, "signup.html", {})


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@ensure_csrf_cookie
def signout(request):
    logout(request)
    messages.success(request,"Logged out")
    return redirect('signin')


def authenticate(username, password):
    if CustomUser.objects.filter(username=username, password=password).exists():
        user = CustomUser.objects.get(username=username)
    else:
        user = None
    return user


def about_me(request):
    return render(request, "aboutme.html", {})

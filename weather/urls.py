from django.urls import path
from weather import views

urlpatterns = [
    path("", view=views.home, name="home"),
    path("signin/", view=views.signin, name="signin"),
    path("signup/", view=views.signup, name="signup"),
    path("signout/", view=views.signout, name="signout"),
    path("aboutme/", view=views.about_me, name="aboutme"),
]

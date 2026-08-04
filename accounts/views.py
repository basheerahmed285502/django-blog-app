from django.shortcuts import render
from .forms import UserRegistrationForm, LoginForm
from .models import UserProfile
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

# Create your views here.


def register(request):
    homeurl = reverse("home")
    if request.user.is_authenticated:
        return HttpResponseRedirect(homeurl)

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(
                user=user,
                phone_number=form.cleaned_data["phone_number"],
                city=form.cleaned_data["city"],
                address=form.cleaned_data["address"]
            )
            return HttpResponseRedirect(homeurl)
    else:
        form = UserRegistrationForm()

     # FIXED INDENTATION HERE: Removed from the 'else' block.
    # This now runs on a GET request OR when a POST request form is invalid.
    return render(request, "accounts/register.html", {"form": form})


def login(request):
    homeurl = reverse("home")
    if request.user.is_authenticated:
        return HttpResponseRedirect(homeurl)

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return HttpResponseRedirect(homeurl)
            else:
                form.add_error(None, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})


def logout(request):
    loginurl = reverse("login")
    auth_logout(request)
    return HttpResponseRedirect(loginurl)

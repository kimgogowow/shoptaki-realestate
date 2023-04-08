from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# from django.utils import timezone
from shoptaki.forms import LoginForm, RegisterForm, FinderForm

# Create your views here.


def home_view(request):
    return render(request, 'shoptaki/home.html')


def login_action(request):
    context = {}
    if request.method == 'GET':
        context['form'] = LoginForm()
        # once passed authentication--jump to global stream
        if request.user.is_authenticated:

            return render(request, 'shoptaki/home.html', context)
        return render(request, 'shoptaki/login.html', context)

    form = LoginForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'shoptaki/login.html', context)

    newUser = authenticate(
        username=form.cleaned_data['username'], password=form.cleaned_data['password'])
    login(request, newUser)
    # update the global stream page
    return redirect(reverse('home'))


def register_action(request):
    context = {}
    # if "get"-display the registerform
    if request.method == "GET":
        context['form'] = RegisterForm()
        return render(request, 'shoptaki/register.html', context)
    # obtain the input and render to the page
    form = RegisterForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'shoptaki/register.html', context)
    # save the input and login
    newUser = User.objects.create_user(username=form.cleaned_data['username'],
                                       # it is pw1!!!!
                                       password=form.cleaned_data['password'],
                                       email=form.cleaned_data['email'],
                                       first_name=form.cleaned_data['first_name'],
                                       last_name=form.cleaned_data['last_name'])
    newUser.save()
    newUser = authenticate(
        username=form.cleaned_data['username'], password=form.cleaned_data['password'])

    login(request, newUser)
    # update the global stream page
    return redirect(reverse('home'))


def logout_action(request):
    logout(request)
    return redirect(reverse('login'))


def finder_action(request):
    context = {}
    if request.method == 'GET':
        context['form'] = FinderForm()
        # once passed authentication--jump to global stream
        return render(request, 'shoptaki/finder.html', context)

    form = FinderForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'shoptaki/finder.html', context)
    # update the global stream page
    return redirect(reverse('home'))


@login_required
def user_profile_action(request):
    context = {}
    if request.method == "GET":
        return render(request, 'shoptaki/profile.html', context)


def find_action(request):
    context = {}
    if request.method == "GET":
        return render(request, 'shoptaki/finder.html', context)


def user_settings_action(request):
    context = {}
    if request.method == "GET":
        return render(request, 'shoptaki/settings.html', context)


def check_favorites(request):
    context = {}
    if request.method == "GET":
        return render(request, 'shoptaki/favorites.html', context)

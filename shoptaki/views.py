from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# from django.utils import timezone
from django.conf import settings
from .forms import LoginForm, RegisterForm, FinderForm
from .models import Listing
from .listing import import_listings_from_csv
import requests
from django.shortcuts import get_object_or_404, render

# Create your views here.


def home_view(request):
    return render(request, 'shoptaki/home.html')


def info_view(request):
    return render(request, 'shoptaki/info.html')


def login_action(request):
    context = {}
    if request.method == 'GET':
        context['form'] = LoginForm()
        context['login_url'] = settings.LOGIN_URL
        # once passed authentication--jump to global stream
        if request.user.is_authenticated:
            return render(request, 'shoptaki/home.html', context)
        return render(request, 'shoptaki/login.html', context)

    form = LoginForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        # context['error_msg'] = "invalid username or password"
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


@login_required
def logout_action(request):
    logout(request)
    return redirect(reverse('login'))


@login_required
def finder_type_action(request):
    context = {"type": request.POST}
    if request.method == "GET":
        return render(request, 'shoptaki/finder_type.html', context)


def finder_action(request):
    context = {}

    if request.method == 'GET':
        type = request.GET.get('type')
        context = {'type': type}
        context['form'] = FinderForm()
        # once passed authentication--jump to global stream
        return render(request, 'shoptaki/finder.html', context)

    form = FinderForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        error = "Sorry Invalid Input"
        context['error'] = error
        return render(request, 'shoptaki/finder.html', context)
    # update the global stream page

    return redirect(reverse('listings'))


@login_required
def user_profile_action(request):
    context = {}
    if request.method == "GET":
        return render(request, 'shoptaki/profile.html', context)

# def listings(request):
#     # context = {}
#     if request.method == "GET":
#         return render(request, 'shoptaki/listings.html', context)


@login_required
def listings(request):
    context = {}
    if request.method == "GET":
        # Call import_listings_from_csv function to import listings from CSV
        import_listings_from_csv('shoptaki/data/listings.csv')
        listings = Listing.objects.all()
        context['listings'] = listings
        return render(request, 'shoptaki/listings.html', context)


def listing(request, listing_address):
    context = {}
    if request.method == "GET":
        listing = get_object_or_404(Listing, address=listing_address)
        context['listing'] = listing
        return render(request, 'shoptaki/listing.html', context)


def check_favorites(request):
    context = {}
    if request.method == "GET":
        return render(request, 'shoptaki/favorites.html', context)


def refresh_listings(request):
    #USED TO CALL API DO NOT CALL UNLESS NEED TO REFRESH WE ONLY HAVE SO MANY PULLS
    Listing.objects.all().delete()
    context={}
    url = "https://zillow56.p.rapidapi.com/search"
    querystring = {"location":"pittsburgh, pa","status":"forSale","isMultiFamily":"true"}
    headers = {
        "content-type": "application/octet-stream",
        "X-RapidAPI-Key": "0376013f28msh9dfa0bf8473d107p1d88d2jsnc21f53b7bdca",
        "X-RapidAPI-Host": "zillow56.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    listings = data['results']
    for i in listings:
        listing_data = Listing(
        address = i.get('streetAddress', "NA"),
        city = i.get('city', "NA"),
        state = i.get('state', "NA"),
        zipcode = i.get('zipcode', "NA"),
        price = i.get('price', -1),
        bedrooms = i.get('bedrooms', -1),
        bathrooms = i.get('bathrooms', -1),
        sqft = i.get('livingArea', -1),
        lot_size = i.get('lotAreaValue',-1),
        days_listed = i.get('daysOnZillow', -1),
        longitude = i.get('longitude', -1),
        latitude = i.get('latitude', -1),
        img = i.get('imgSrc', ""),
        rent_estimate = i.get('rentZestimate', -1)
        )

        listing_data.save()
    all_listings = Listing.objects.all()
    context['listings'] = all_listings
    return render(request, 'shoptaki/listings.html', context)
def get_listings(request):
    context={}
    all_listings = Listing.objects.all()
    context['listings'] = all_listings
    return render(request, 'shoptaki/listings.html', context)



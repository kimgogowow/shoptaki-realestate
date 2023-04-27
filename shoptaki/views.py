import decimal
import numpy as np
import numpy_financial as npf
from decimal import Decimal

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# from django.utils import timezone
from django.conf import settings
from .forms import LoginForm, RegisterForm, FinderForm
from .models import Listing, Analytics, ListingAnalytics
from .listing import import_listings_from_csv
import requests
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

# Create your views here.


""" def _pic_check(action_function):
    context = {}
    if request.method == 'GET':
        pic = request.user.social_auth.get(
            provider='google-oauth2').extra_data['picture']
        context['pic'] = pic
    return render(request, 'shoptaki/base.html', context)
 """

def home_view(request):
    context = {}
    if request.method == 'GET':
        pic = request.user.social_auth.get(
            provider='google-oauth2').extra_data['picture']
        context['pic'] = pic

    # context = {}
    # if request.method == 'GET':
    #    pic = request.user.social_auth.get(
    #        provider='google-oauth2').extra_data['picture']
    #    context['pic'] = pic
    return render(request, 'shoptaki/home.html', context)


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
        pic = request.user.social_auth.get(
            provider='google-oauth2').extra_data['picture']
        context['pic'] = pic
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
        analytics = Analytics.objects.first()
        loan_to_val = analytics.loan_to_value*0.01
        cap_rate = analytics.cap_rate * 0.01
        interest_rate = analytics.interest_rate*0.01
        loan_amount = listing.price * decimal.Decimal(loan_to_val)
        cash_invested = listing.price - loan_amount
        noi = listing.price * decimal.Decimal(cap_rate)
        p_interest = loan_amount * decimal.Decimal(interest_rate)
        p_fcf = noi - p_interest
        per = np.arange(1*12) + 1
        payment_per_month = np.repeat(abs(npf.pmt(decimal.Decimal(
            interest_rate)/12, 20*12, decimal.Decimal(loan_amount))), 12)
        interest_per_month = abs(npf.ipmt(decimal.Decimal(
            interest_rate)/12, per, 20*12, loan_amount))
        principal_per_month = np.subtract(
            payment_per_month, interest_per_month)
        principal_pandi = round(np.sum(principal_per_month), 2)
        interest_pandi = round(np.sum(interest_per_month), 2)
        free_cash_flow_pandi = round(decimal.Decimal(
            noi) - decimal.Decimal(interest_pandi) - decimal.Decimal(principal_pandi), 2)
        cash_on_cash_pandi = round(
            (decimal.Decimal(free_cash_flow_pandi)/decimal.Decimal(cash_invested)) * 100, 2)
        debt_yield_pandi = round(
            (decimal.Decimal(noi)/decimal.Decimal(loan_amount)) * 100, 2)
        debt_constant_pandi = round(((decimal.Decimal(
            interest_pandi)+decimal.Decimal(principal_pandi))/decimal.Decimal(loan_amount)) * 100, 2)

        listing_info = ListingAnalytics(
            noi=noi.quantize(decimal.Decimal('.01')),
            monthly_noi=(noi / 12).quantize(decimal.Decimal('.01')),
            p_interest=p_interest.quantize(decimal.Decimal('.01')),
            p_fcf=p_fcf.quantize(decimal.Decimal('.01')),
            p_cashoncash=((p_fcf/cash_invested) *
                          100).quantize(decimal.Decimal('.01')),
            p_debtyield=((noi/loan_amount) *
                         100).quantize(decimal.Decimal('.01')),
            p_debtconstant=((p_interest/loan_amount) *
                            100).quantize(decimal.Decimal('.01')),
            pandi_principal=principal_pandi,
            pandi_interest=interest_pandi,
            pandi_fcf=free_cash_flow_pandi,
            pandi_cashoncash=cash_on_cash_pandi,
            pandi_debtyield=debt_yield_pandi,
            pandi_debtconstant=debt_constant_pandi

        )
        context['listing'] = listing
        context['analytics'] = analytics
        context['listing_info'] = listing_info

        return render(request, 'shoptaki/listing.html', context)


def check_favorites(request):
    context = {}
    if request.method == "GET":
        return render(request, 'shoptaki/favorites.html', context)


def refresh_listings(request):
    # USED TO CALL API DO NOT CALL UNLESS NEED TO REFRESH WE ONLY HAVE SO MANY PULLS
    Listing.objects.all().delete()
    context = {}
    url = "https://zillow56.p.rapidapi.com/search"
    querystring = {"location": "pittsburgh, pa",
                   "status": "forSale", "isMultiFamily": "true"}
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
            address=i.get('streetAddress', "NA"),
            city=i.get('city', "NA"),
            state=i.get('state', "NA"),
            zipcode=i.get('zipcode', -1),
            price=i.get('price', -1),
            bedrooms=i.get('bedrooms', -1),
            bathrooms=i.get('bathrooms', -1),
            sqft=i.get('livingArea', -1),
            lot_size=i.get('lotAreaValue', -
                           1).quantize(decimal.Decimal('.01')),
            days_listed=i.get('daysOnZillow', -1),
            longitude=i.get('longitude', -1),
            latitude=i.get('latitude', -1),
            img=i.get('imgSrc', ""),
            rent_estimate=i.get('rentZestimate', -1)
        )
        listing_data.save()
    all_listings = Listing.objects.all()
    context['listings'] = all_listings
    return render(request, 'shoptaki/listings.html', context)


def get_results(request):
    Analytics.objects.all().delete()
    context = {}
    if request.method == "POST":
        form = request.POST
        current_savings = Decimal(form['current_savings'])
        result_listings = []
        all_listings = Listing.objects.all()
        for listing in all_listings:
            if listing.price <= current_savings:
                result_listings.append(listing)
        form_data = Analytics(
            cap_rate=Decimal(form['cap_rate']),
            loan_to_value=Decimal(form['loan_to_value']),
            current_savings=Decimal(form['current_savings']),
            interest_rate=Decimal(form['interest_rate']),
            amort_sched=Decimal(form['amort_sched']),
        )
        form_data.save()
        context['listings'] = result_listings
        context['analytics'] = form_data
        return render(request, 'shoptaki/listings.html', context)

    else:
        form = FinderForm()
    return render(request, "shoptaki/finder.html", {"form": form})

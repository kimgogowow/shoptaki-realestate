"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from shoptaki import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home_view, name="home"),
    path('oauth/', include('social_django.urls', namespace='social')),
    # path('logout', auth_views.logout_then_login, name='logout'),
    path('info', views.info_view, name="info"),
    path('login', views.login_action, name="login"),
    path('register', views.register_action, name="register"),
    path('logout', views.logout_action, name="logout"),
    path('finder_type', views.finder_type_action, name="finder_type"),
    path('finder', views.finder_action, name="finder"),
    path('favorites', views.check_favorites, name="favorites"),
    path('profile', views.user_profile_action, name="profile"),
    path('listings', views.get_listings, name="listings"),
    path('listing/<str:listing_address>/', views.listing, name='listing'),
    path('refresh_listings', views.refresh_listings, name="refresh_listings"),#API CALL USE SPARINGLY
]

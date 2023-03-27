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
from django.urls import path
from shoptaki import views


urlpatterns = [
    path('',views.home_page,name="home"),
    path('login', views.login_action, name="login"),
    path('register', views.register_action, name="register"),
    path('logout', views.logout_action, name="logout"),
    path('my_profile', views.user_profile_action, name="my_profile"),
    path('finder', views.property_action, name="finder"),
 
]

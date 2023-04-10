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
    path('', views.home_view, name="home"),
    path('info',views.info_view,name="info"),
    path('login', views.login_action, name="login"),
    path('register', views.register_action, name="register"),
    path('logout', views.logout_action, name="logout"),
    path('finder', views.find_action, name="finder"),
    path('favorites', views.check_favorites, name="favorites"),
    path('profile', views.user_profile_action, name="profile"),
    path('settings', views.user_settings_action, name="settings"),

]

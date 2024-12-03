from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('signout', views.signout, name='signout'),
    path('reset_password', views.reset_password, name='reset_password')
]

# creating path for the functions in views.py which will be directly adressed by the template and the urls.py in myCWK folder
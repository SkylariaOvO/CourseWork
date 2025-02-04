from django.contrib import admin
from django.urls import path,include
from django.http import HttpResponse
from . import views


# creating path for the functions in views.py which will be directly adressed by the template and the urls.py in myCWK folder

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.signin, name='login'),
    path('logout/', views.signout, name='logout'),
    path('password-reset/', views.request_reset_password, name='password_reset_request'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
    path('password-reset/<uidb64>/<token>/', views.reset_password, name='password_reset'),
]

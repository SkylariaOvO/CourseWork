from django.contrib import admin
from django.urls import path,include
from django.http import HttpResponse


from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.signin, name='login'),
    path('signout/', views.signout, name='signout'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate')
]



# creating path for the functions in views.py which will be directly adressed by the template and the urls.py in myCWK folder
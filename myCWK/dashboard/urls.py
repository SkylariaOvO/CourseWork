from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path('', views.home, name='home'),
    path('my_posts/', views.my_posts, name='my_posts'),
    path('my_events/', views.my_events, name='my_events'),
    path('settings/', views.settings, name='settings'),
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('profile/<str:username>/', views.profile, name='public_profile'),
]

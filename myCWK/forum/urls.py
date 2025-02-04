from django.urls import path
from . import views

urlpatterns = [
    path('', views.forum_home, name='forum_home'),  # List all posts 
  path('create/', views.create_post, name='create_post'),  # Add a new post
  path('<slug:slug>/', views.post_detail, name='post_detail'),  # View a post
]

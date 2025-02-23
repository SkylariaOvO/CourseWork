from django.contrib.auth import models
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.utils.timezone import now
from django.contrib.auth.models import User
from django import forms
import pandas as pd
from forum.models import Post,Reply
from timetable.models import StudySession

@login_required
def home(request):
    return render(request, 'dashboard/home.html')

@login_required
def profile(request):
    return render(request, 'dashboard/profile.html')

@login_required
def settings(request):
    return render(request, 'dashboard/settings.html')

@login_required
def home(request):
    return render(request, 'dashboard/home.html')

@login_required
def my_posts(request):
    """Displays the logged-in user's posts."""
    user_posts = Post.objects.filter(author=request.user)
    return render(request, "dashboard/my_posts.html", {"posts": user_posts})

@login_required
def my_events(request):
    events = StudySession.objects.filter(student=request.user)
    return render(request, 'dashboard/my_events.html', {'events': events})




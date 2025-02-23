from django.contrib.auth import models
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from forum.models import *
from timetable.models import *

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
    posts = Post.objects.filter(author=request.user)
    return render(request, 'dashboard/my_posts.html', {'posts': posts})

@login_required
def my_events(request):
    events = StudySession.objects.filter(student=request.user)
    return render(request, 'dashboard/my_events.html', {'events': events})

@login_required
def my_responses(request):
    responses = ForumResponse.objects.filter(user=request.user)
    return render(request, 'dashboard/my_responses.html', {'responses': responses})

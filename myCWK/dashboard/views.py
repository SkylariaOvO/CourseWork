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
from django.contrib.auth import update_session_auth_hash


@login_required
def home(request):
    return render(request, 'dashboard/home.html')

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


@login_required
def profile(request, username=None):
    # Determine whose profile to display
    if username is None or username == request.user.username:
        profile_user = request.user
        is_owner = True
    else:
        profile_user = get_object_or_404(User, username=username)
        is_owner = False

    # Process the form only if the logged-in user is editing their own profile.
    if is_owner and request.method == "POST":
        username_input = request.POST.get("username", "").strip()
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        bio = request.POST.get("bio", "").strip()
        new_password = request.POST.get("new_password", "")
        confirm_password = request.POST.get("confirm_password", "")
        profile_picture = request.FILES.get("profile_picture")

        # Update User fields
        profile_user.username = username_input
        profile_user.first_name = first_name
        profile_user.last_name = last_name
        profile_user.save()

        # Update profile fields (assuming a OneToOneField named 'profile' exists)
        profile = profile_user.profile
        profile.bio = bio
        if profile_picture:
            profile.profile_picture = profile_picture
        profile.save()

        # Handle password change
        if new_password or confirm_password:
            if new_password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return redirect('dashboard:profile')
            else:
                profile_user.set_password(new_password)
                profile_user.save()
                update_session_auth_hash(request, profile_user)
                messages.success(request, "Password updated successfully.")

        messages.success(request, "Profile updated successfully!")
        return redirect('dashboard:profile')

    # If viewing someone else's profile, get their posts for display.
    user_posts = Post.objects.filter(author=profile_user) if not is_owner else None

    context = {
        'profile_user': profile_user,
        'is_owner': is_owner,
        'user_posts': user_posts,
    }
    return render(request, 'dashboard/profile.html', context)

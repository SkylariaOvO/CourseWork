from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import re
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_str, force_bytes
from django.utils.timezone import now, timedelta
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives, send_mail
from django.conf import settings

Cooldown_Time = timedelta(minutes=1)

from forum.models import Post, Reply
from timetable.models import StudySession

def home(request):
    top_posts = sorted(Post.objects.all(), key=lambda post: post.total_votes(), reverse=True)[:5]

    upcoming_sessions = StudySession.objects.filter(
        student=request.user,
        date__gte=now().date(),
        date__lte=now().date() + timedelta(days=7)
    ).order_by("date", "start_time")

    return render(request, 'index.html', {
        'top_posts': top_posts,
        'upcoming_sessions': upcoming_sessions
    })


# Send Activation Email
def send_activation_email(user, request):
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    activation_link = f"{request.scheme}://{request.get_host()}/activate/{uidb64}/{token}/"

    email_body = render_to_string("emails/activation_email.html", {
        "username": user.username,
        "activation_link": activation_link,
    })

    email = EmailMultiAlternatives(
        subject="Activate Your Account",
        body=email_body,
        from_email=settings.EMAIL_HOST_USER,
        to=[user.email]
    )
    email.attach_alternative(email_body, "text/html")
    email.send()

# Account Activation
def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated successfully!")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid or has expired.")
        return redirect('register')

# Registration Validation
def validate_registration(request, username, email, password, password2):
    if User.objects.filter(username=username).exists():
        messages.error(request, 'Username already exists.')
        return False
    if User.objects.filter(email=email).exists():
        messages.error(request, 'Email already exists.')
        return False
    if password != password2:
        messages.error(request, 'Passwords do not match.')
        return False
    if not re.match(r'^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
        messages.error(request, 'Password must be strong.')
        return False
    return True

# User Registration
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        profile_picture = request.FILES.get('profile_picture')

        if validate_registration(request, username, email, password, password2):
            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.is_active = False  # Email verification switch
                user.save()

                # PFP stuff
                profile = user.profile
                if profile_picture:
                    profile.profile_picture = profile_picture
                else:
                    profile.profile_picture = 'default.png'  # Assign default if no picture
                profile.save()

                send_activation_email(user, request)
                messages.success(request, 'Account created! Check your email to activate.')
                return redirect('login')
            except Exception as e:
                messages.error(request, f'An error occurred: {e}')
                return redirect('register')

    return render(request, 'register.html')

# User Sign-in
def signin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Invalid Credentials")
            return redirect("login")

        user = authenticate(request, username=user.username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid Credentials")
            return redirect("login")

    return render(request, 'login.html')

# User Sign-out
def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully")
    return redirect("home")

# Password Reset Request
def request_reset_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
      
        last_reset_time = request.session.get("last_password_reset")
        if last_reset_time:
          last_reset_time = now() - timedelta(seconds=last_reset_time) 
          if now() < last_reset_time + Cooldown_Time:  
              messages.error(request, "You must wait before requesting another password reset.")
              return redirect("password_reset_request")

        try:
            user = User.objects.get(email=email)
            send_reset_email(user, request)
            request.session["last_password_reset"] = now().timestamp()
            messages.success(request, "Password reset email sent. Check your inbox.")
        except User.DoesNotExist:
            messages.error(request, "No account found with that email.")
        return redirect("password_reset_request")
    return render(request, "request_reset_password.html")

# Send Password Reset Email
def send_reset_email(user, request):
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    reset_link = f"{request.scheme}://{request.get_host()}/password-reset/{uidb64}/{token}/"

    email_body = render_to_string("emails/reset_password_email.html", {
        "username": user.username,
        "reset_link": reset_link,
    })

    email = EmailMultiAlternatives(
        subject="Reset Your Password",
        body=email_body,
        from_email=settings.EMAIL_HOST_USER,
        to=[user.email]
    )
    email.attach_alternative(email_body, "text/html")
    email.send()

# Reset Password Form
def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == "POST":
            password = request.POST.get("password")
            password2 = request.POST.get("password2")

            if password != password2:
                messages.error(request, "Passwords do not match.")
            elif not re.match(r'^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
                messages.error(request, "Password must meet complexity requirements.")
            else:
                user.set_password(password)
                user.save()
                messages.success(request, "Password reset successful. You can now log in.")
                return redirect("login")

        return render(request, "reset_password.html", {"uidb64": uidb64, "token": token})
    else:
        messages.error(request, "Password reset link is invalid or expired.")
        return redirect("password_reset_request")

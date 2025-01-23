from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import re
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_str, force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator


def home(request):
    return render(request, 'index.html')


from django.core.mail import send_mail
from django.conf import settings

def send_registration_email(to_email, username):
    subject = 'Welcome to Rugby School Academic Discussion Forum'
    message = f'Hi {username},\n\nThank you for registering at our platform. We are excited to have you!\n\nBest Regards,\nTeam'
    from_email = settings.EMAIL_HOST_USER

    send_mail(subject, message, from_email, [to_email])

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

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if validate_registration(request, username, email, password, password2):
            try:
                # Create user but set is_active to False
                user = User.objects.create_user(username=username, email=email, password=password)
                user.is_active = False
                user.save()

                # Generate activation link
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                activation_link = f"{request.scheme}://{request.get_host()}/activate/{uidb64}/{token}/"
                email_body = render_to_string("emails/activation_email.html", {"username" : username, "activation_link" : activation_link,})

              # Send activation email
                send_mail(
                    'Activate Your Account',
                    email_body,
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )

                messages.success(request, 'Account created successfully! Please check your email to activate your account.')
                return redirect('login')
            except Exception as e:
                messages.error(request, f'An error occurred: {e}')
                return redirect('register')
    return render(request, 'register.html')

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
        messages.error(request, 'Password must be at least 8 characters long, include an uppercase letter, a lowercase letter, a number, and a special character.')
        return False
    return True
  
def signin(request):

  if request.method == "POST":
    email = request.POST['email']
    password = request.POST['password']

    try: 
      user = User.objects.get(email=email)
    except User.DoesNotExist:
      messages.error(request,"Invalid Credentials")
      return redirect("/login")



    user = authenticate(request, username = user.username, password=password)



    if user is not None:
      login(request, user)
      username = user.username
      return render(request, "index.html",{"username":username})

    else:
      messages.error(request,"Invalid Credentials")
      return redirect("login")

  return render(request, 'login.html')


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully")
    return redirect("home")

# Reset password (implement this function using Django's password reset views for better security)
def forgot_password(request):
    # implementation needed
    return render(request, "forgot_password.html")

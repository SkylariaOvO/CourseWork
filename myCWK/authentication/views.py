from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
import re  

def home(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('register')

        if password != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        # Check password strength
        if not re.match(r'^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
            messages.error(request, 'Password must be at least 8 characters long, include an uppercase letter, a lowercase letter, a number, and a special character.')
            return redirect('register')

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'An error occurred: {e}')
            return redirect('register')

    return render(request, 'register.html')


# Login user
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
  messages.success(request,"Logged Out Successfully")
  return redirect("index")
  
# Reset password
def forgot_password(request):
  """
    if request.method == "POST":
        username = request.POST['username']
        new_password = request.POST['password']
        hashed_password = hash_password(new_password)

        if not user_exists(username):
            return render(request, 'auth.html', {'error': 'Username does not exist.'})

        with connection.cursor() as cursor:
            cursor.execute("UPDATE UserTbl SET password_hash = %s WHERE username = %s", [hashed_password, username])
        return redirect('login')

  """

  return render(request, "forgot_password.html")

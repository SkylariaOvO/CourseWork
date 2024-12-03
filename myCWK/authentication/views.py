import hashlib
from django.shortcuts import render, redirect
from django.db import connection

def home(request):
  return render(request, 'index.html')

# Hash password function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Check if a user exists
def user_exists(username):
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1 FROM UserTbl WHERE username = %s", [username])
        return cursor.fetchone() is not None

# Register user
def register(request):
  """
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        if user_exists(username):
            return render(request, 'auth.html', {'error': 'Username already exists.'})

        hashed_password = hash_password(password)
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO UserTbl (username, password_hash) VALUES (%s, %s)", [username, hashed_password])
        return redirect('login')
  """

  return render(request, "register.html")

# Login user
def login(request):
  """
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        hashed_password = hash_password(password)

        with connection.cursor() as cursor:
            cursor.execute("SELECT password_hash FROM UserTbl WHERE username = %s", [username])
            result = cursor.fetchone()
            if result and result[0] == hashed_password:
                return render(request, 'auth.html', {'success': 'Login successful!'})
            return render(request, 'auth.html', {'error': 'Invalid username or password.'})

  """

  return render(request, "login.html")

def signout(request):
    pass
  
# Reset password
def reset_password(request):
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

  return render(request, "reset_password.html")

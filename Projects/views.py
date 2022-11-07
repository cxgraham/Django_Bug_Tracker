from django.shortcuts import render, redirect
from django.contrib import messages

from .models import User
import bcrypt

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'GET':
        return render(request, 'login_register.html')
    if request.method == 'POST':
        errors = User.objects.user_validator(request.POST)
        if len(errors) > 0:
            print(errors)
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/register')
        else:
            email = request.POST['email'].lower()
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            print(pw_hash)
            created_user = User.objects.create(first_name = request.POST['first_name'], email = email, password = pw_hash)
            created_user.save()
            print(created_user)
            return redirect('/')

def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0]
        print(logged_user)
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
        return redirect('/')
    return redirect('/')



# Create your views here.

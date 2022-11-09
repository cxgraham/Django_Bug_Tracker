from hashlib import new
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import User, Project, Bug
import bcrypt


# CREATE 

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
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
            request.session['first_name'] = created_user.first_name
            request.session['user_id'] = created_user.id
            created_user.save()
            print(created_user)
            return redirect('/homepage')

def new_project(request):
    if request.method == 'GET':
        return render(request, 'new_project.html')
    if request.method == 'POST':
        title = request.POST['title']
        details = request.POST['description']
        this_user = User.objects.get(id = request.session['user_id'])
        new_project = Project.objects.create(title = title, description = details, user = this_user)
        request.session['project'] = new_project
        new_project.save()
        return redirect('/homepage')



# READ 

def index(request):
    return render(request, 'loginpage.html')

def homepage(request):
    this_user = User.objects.get(id = request.session['user_id'])
    context = {
        'first_name': this_user.first_name,
        'projects': this_user.projects.all(),
    }
    print(this_user.projects)
    return render(request, 'homepage.html', context)

def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0]
        print(logged_user)
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            request.session['first_name'] = logged_user.first_name
        return redirect('/homepage')
    return redirect('/')



# UPDATE 




# DELETE

def logout(request):
    request.session.flush()
    return redirect('/')

# Create your views here.

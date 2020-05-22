from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, "index.html")

def register(request):
    errors = User.objects.form_validation(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else: 
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = pw_hash,
            birthdate = request.POST['birthdate']
        )

    return redirect('/')

def login(request):
    users = User.objects.all()
    user = User.objects.filter(email=request.POST['email_log'])
    errors = User.objects.login_validation(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    if user: 
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password_log'].encode(), logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            return redirect(f'/wall/')

    return redirect('/')

def success(request):
    context = {
        "an_user" : User.objects.get(id=request.session['userid'])
    }
    return render(request, "wall.html", context)


def logout(request):
    request.session.flush()
    return redirect('/')

from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages

def wall_home(request): 
    context = {
        "an_user" : User.objects.get(id=request.session['userid']),
        "number" : request.session['userid'],
        "messages" : Message.objects.all().order_by('created_at').reverse(),
        "users" : User.objects.all()
    }
    return render(request, "wall.html", context)


def newMessage(request):
    user = User.objects.get(id=request.POST['id'])
    new_message = user.messages.create(
        message = request.POST['message'],
        user = user
    )
    return redirect('/wall')

def newComment(request):
    message = Message.objects.get(id=request.POST['noise'])
    print(request.POST['noise'])
    new_comment = message.comments.create(
        comment = request.POST['comment'],
        user = User.objects.get(id=request.session['userid']),
        message = message
    )
    return redirect('/wall')
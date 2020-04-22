from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, 'index.html')

def register(request):
    return render(request, 'register.html')

def table_update(request):
    if 'userid' not in request.session:
        return redirect('/')
    else: 
        context = {
        "user": User.objects.get(id=request.session['userid']),
        }
    return render(request, 'table_update.html', context)

def create(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect ('/register')
    else:
        if request.method == 'POST':
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            newuser = User.objects.create(first_name = request.POST["first_name"], 
            last_name = request.POST["last_name"], 
            email = request.POST["email"], 
            password=pw_hash
            )
            request.session["userid"] = newuser.id
        return redirect('/tasks') 

def login(request):
    user = User.objects.filter(email=request.POST['email_login']) 
    if user: 
        logged_user = user[0] 
        if bcrypt.checkpw(request.POST['password_login'].encode(), logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            return redirect('/tasks')
    return redirect('/')

def reset(request):
    request.session.clear()
    return redirect('/')

def appointment(request):
    if 'userid' not in request.session:
        return redirect('/')
    else: 
        context = {
        "user": User.objects.get(id=request.session['userid']),
        }
        return render(request, 'appointments.html', context)

def addroute(request):
    if 'userid' not in request.session:
        return redirect('/')
    return render(request, 'add.html')

def adding(request):
    errors = Appointment.objects.epic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect ('/tasks/add')
    else:
        if request.method == 'POST':
            Appointment.objects.create(
                task = request.POST["task"], 
                date = request.POST["date"], 
                status = request.POST["status"], 
                user = User.objects.get(id = request.session['userid']
            ))
        return redirect('/tasks')

def edit_route(request, id):
    if 'userid' not in request.session:
        return redirect('/')
    context = {
        "edit": Appointment.objects.get(id=id)
    }
    return render(request, "edit.html", context)

def update(request, id):
    errors = Appointment.objects.epic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect ('/tasks/' + str(id))
    if request.method == 'POST':
        change = Appointment.objects.get(id=id)
        change.task = request.POST["task"]
        change.date = request.POST["date"]
        change.status = request.POST["status"]
        change.save()
    return redirect('/update/table') 

def delete(request, id):
    destroy = Appointment.objects.get(id=id)
    if destroy.status in {"Done", "Missed", "Pending"} and request.session["userid"] == destroy.user.id:
        destroy.delete()
    return redirect('/update/table')


from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt

# CREATE NEW USER
def create(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        print(errors)
        return redirect('/')
    else:
        pass_hash = bcrypt.hashpw(request.POST['password'].encode('utf-8'), bcrypt.gensalt())
        user = User.objects.create(username = request.POST['username'], name = request.POST['name'], password = pass_hash.decode('utf-8'))
        request.session['id'] = user.id
        request.session['name'] = user.name
        return redirect('/dash')

# USER DASHBOARD PAGE
def dash(request):
    try:
        all_plans = Travel.objects.exclude(planned_users = User.objects.get(id=request.session['id']))
        your_plans = Travel.objects.filter(planned_users = User.objects.get(id=request.session['id']))
        context = {
            'all_plans': all_plans,
            'your_plans': your_plans
        }
        return render(request, 'travel_buddy/dash.html', context)
    except KeyError:
        return redirect('/')

# LOGIN / REGISTRATION PAGE
def index(request):
    return render(request, 'travel_buddy/index.html')

# JOIN PROCESS
def join(request, id):
    user = User.objects.get(id=request.session['id'])
    plan = Travel.objects.get(id=id)
    user.user_plans.add(plan)
    user.save()
    return redirect('/dash')

# LOGOUT PROCESS
def logout(request):
    request.session.clear()
    return redirect('/')

# LOGIN PROCESS
def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        print(errors)
        return redirect('/')
    else:
        user = User.objects.get(username=request.POST['username'])
        if bcrypt.checkpw(request.POST['password'].encode('utf-8'), user.password.encode('utf-8')):
            request.session['id'] = user.id
            request.session['username'] = user.username
            return redirect('/dash')
        else:
            messages.error(request, 'Incorrect password.')
            return redirect('/')

# PLAN PAGE
def plan(request, id):
    plan = Travel.objects.get(id=id)
    creator_id = plan.created_by.id
    user_list = User.objects.exclude(id = creator_id).filter(user_plans = plan)
    print(user_list)
    context = {
        'plan': plan,
        'user_list': user_list
    }
    return render(request, 'travel_buddy/plan.html', context)

# ADD TRAVEL PAGE
def add_travel(request):
    return render(request, 'travel_buddy/add_travel.html')

# ADD TRAVEL PROCESS
def process_travel(request):
    errors = Travel.objects.travel_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/add_travel')
    else:
        new_travel = User.objects.get(id=request.session['id']).user_plans.create(destination = request.POST['destination'], description = request.POST['description'], travel_from = request.POST['travel_from'], travel_to = request.POST['travel_to'], created_by = User.objects.get(id=request.session['id']))
        return redirect('/dash')

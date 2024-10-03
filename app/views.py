import random
from django.shortcuts import get_object_or_404, redirect, render
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from app.forms import CustomUserCreationForm, TaskForm
from app.models import Task
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
# Create your views here.
def home(request):
    return render(request, 'home.html')
def login_view(request):
    if request.method == "POST":
        #it checks if password is same or not ,and the username will be checked
        form = AuthenticationForm(request, data=request.POST)
        print(form.errors)

        print(form.is_valid())
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful. You are now logged in.')
            return redirect('home')  # Redirect to your dashboard or success page
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.capitalize()}: {error}')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == "POST":
        #built in form to create the user
        #this is built in so the uniqueness will be handled by it
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('home')  # Redirect to your dashboard or success page
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.capitalize()}: {error}')
    else:
        initial_data={'username':'','email':'','password1':'','password2':''}
        form = UserCreationForm(initial_data)
    
    return render(request, 'registration.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')

def task_list(request):
    tasks = Task.objects.all().order_by('due_date')
    return render(request, 'task_list.html', {'tasks': tasks})
@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'task_form.html', {'form': form})
@login_required
def task_update(request, id):
    task = get_object_or_404(Task, id=id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_form.html', {'form': form})
@login_required
def task_delete(request, id):
    task = get_object_or_404(Task, id=id)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'task_delete.html', {'task': task})

def task_detail(request, id):
    task = get_object_or_404(Task, id=id)
    return render(request, 'task_detail.html', {'task': task})

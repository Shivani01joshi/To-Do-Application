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

# Create your views here.
def home(request):
    return render(request, 'home.html')
def send_otp(request, email):
    otp = random.randint(100000, 999999)
    request.session['otp'] = str(otp)  
    subject = "Your OTP is"
    message = f"Your OTP is {otp}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
    return otp

def Sign_up(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            request.session['form_data'] = form.cleaned_data 
            send_otp(request, email)  
            request.session['email'] = email
            return redirect('verify_otp')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration.html', {'form': form})

def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        correct_otp = request.session.get('otp')
        if entered_otp == correct_otp:
            form_data = request.session.get('form_data')
            if form_data:
                form = CustomUserCreationForm(form_data)
                if form.is_valid():
                    user = form.save()
                    messages.success(request, 'Account created successfully.')
                    return redirect('login')
                else:
                    messages.error(request, 'Form validation failed.')
            else:
                messages.error(request, 'Form data is missing.')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')

    return render(request, 'verify_otp.html')

def verify_otp_login(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        correct_otp = request.session.get('otp')
        username = request.session.get('username')
        password = request.session.get('password')
        if entered_otp == correct_otp:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'OTP verified successfully.')
                return redirect('home')  
            else:
                messages.error(request, 'Authentication failed.')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
    return render(request, 'verify_otp_login.html')


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                email = user.email
                request.session['username'] = username
                request.session['password'] = password
                request.session['email'] = email
                send_otp(request, email)
                messages.success(request, 'OTP has been sent to your email.')
                return redirect('verify_otp_login')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Authentication failed')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

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

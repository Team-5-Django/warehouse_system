from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import *
from django.contrib import messages

# Login View
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    form = LogInForm(request, data=request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.user.is_staff:
                return redirect('dashboard')
            else:
                return redirect('home')    
    
    return render(request, 'users/login.html', {'form': form})

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

# Signup View (Only employees can sign up)
def signup(request):
    # if request.user.is_authenticated:
    #     return redirect('dashboard')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'employee'  # Set default role as employee
            user.save()
            login(request, user) 
            return redirect('dashboard')  
    else:
        form = SignUpForm()
    
    return render(request, 'users/signup.html', {'form': form})

# Dashboard (Accessible by all admin)
@login_required
@user_passes_test(lambda u: u.is_manager(), login_url='home') 
def dashboard(request):
    return render(request, "users/dashboard.html")

@login_required
def add_user(request):
    if not request.user.is_manager():
        return redirect('dashboard')

    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password']) 
            user.save()
            return redirect('dashboard') 
    else:
        form = AddUserForm()

    return render(request, 'users/add_user.html', {'form': form})

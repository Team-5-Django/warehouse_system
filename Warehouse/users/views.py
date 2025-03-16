from .forms import *
from django.urls import reverse 
from django.contrib import messages
from django.shortcuts import render, redirect 
from .models import PendingUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test


# Login View
def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('dashboard'))  
    
    form = LogInForm(request, data=request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:  
                return redirect(reverse('dashboard')) 
            else:
                return redirect('home') 
    return render(request, 'users/login.html', {'form': form})


# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')


# Signup View (Only employees can sign up)
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            PendingUser.objects.create(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )
            messages.success(request, "Your request has been sent to the admin for approval.")
            return redirect('home')  
    
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



# Accept or Reject user
def is_admin(user):
    return user.is_staff 
@login_required
@user_passes_test(is_admin)
def approve_users(request):
    pending_users = PendingUser.objects.all()
    return render(request, 'users/approve_users.html', {'pending_users': pending_users})
@login_required
@user_passes_test(is_admin)
def approve_user(request, user_id):
    pending_user = PendingUser.objects.get(id=user_id)
    
    User.objects.create(
        username=pending_user.username,
        email=pending_user.email,
        password=make_password(pending_user.password) 
    )
    pending_user.delete()  
    messages.success(request, f"User {pending_user.username} has been approved.")
    return redirect('approve_users')
@login_required
@user_passes_test(is_admin)
def reject_user(request, user_id):
    pending_user = PendingUser.objects.get(id=user_id)
    pending_user.delete()
    messages.warning(request, f"User {pending_user.username} has been rejected.")
    return redirect('approve_users')
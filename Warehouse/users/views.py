from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import make_password
from .forms import LogInForm, SignUpForm, AddUserForm , ChangePasswordForm ,UserEditForm
from django.contrib.auth import update_session_auth_hash
from .models import PendingUser, User


# Helper function to check if the user is an admin
def is_admin(user):
    return user.is_staff


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
            return redirect(reverse('dashboard')) 
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
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                messages.error(request, "Username already exists.")
            else:
                PendingUser.objects.create(
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password1']
                )
                messages.success(request, "Your request has been sent to the admin for approval.")
                return redirect(reverse('login'))
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})

# Edit Profile View (Only logged-in users can edit their profile)
@login_required
def edit_profile(request):
    user = request.user  # Current logged-in user
    form = ChangePasswordForm(user)

    if request.method == "POST":
        form = ChangePasswordForm(user, request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data["new_password1"])
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password has been updated successfully!")
            return redirect("edit_profile")
        else:
            messages.error(request, "Please correct the errors below.")
    return render(request, "users/edit_profile.html", {"user": user, "form": form})



# Delete Account View
@login_required
def delete_account(request):
    user = request.user
    user.delete()  
    logout(request) 
    messages.success(request, "Your account has been deleted successfully.")
    return redirect("home")  


# Add User View (Only managers can add users)
@login_required
def add_user(request):
    if not request.user.is_manager:
        return redirect(reverse('dashboard'))
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect(reverse('approve_users'))
    else:
        form = AddUserForm()
    return render(request, 'users/add_user.html', {'form': form})


# Approve Users View (Only admins can approve users)
@login_required
@user_passes_test(is_admin)
def approve_users(request):
    pending_users = PendingUser.objects.all() 
    all_users = User.objects.exclude(id=request.user.id) 

    return render(request, 'users/approve_users.html', {
        'pending_users': pending_users,
        'all_users': all_users
    })

# Approve a Specific User (Only admins can approve users)
@login_required
@user_passes_test(is_admin)
def approve_user(request, user_id):
    pending_user = get_object_or_404(PendingUser, id=user_id)

    User.objects.create(
        username=pending_user.username,
        email=pending_user.email,
        password=make_password(pending_user.password)
    )
    pending_user.delete()
    messages.success(request, f"User {pending_user.username} has been approved.")
    return redirect('approve_users')


# Reject a Specific User (Only admins can reject users)
@login_required
@user_passes_test(is_admin)
def reject_user(request, user_id):
    pending_user = get_object_or_404(PendingUser, id=user_id)
    pending_user.delete()
    messages.warning(request, f"User {pending_user.username} has been rejected.")
    return redirect('approve_users')



# Delete User By Admin
@login_required
@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user == request.user:
        messages.error(request, "You cannot delete your own account!")
    else:
        user.delete()
        messages.success(request, f"User {user.username} has been deleted successfully.")
    
    return redirect("approve_users") 

# Edit User by Admin
@login_required
@user_passes_test(is_admin)
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == "POST":
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f"User {user.username}'s details have been updated successfully.")
            return redirect("approve_users")
    else:
        form = UserEditForm(instance=user)

    return render(request, "users/edit_user.html", {"form": form, "user": user})
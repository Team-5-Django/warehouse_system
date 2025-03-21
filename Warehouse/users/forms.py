from .models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import check_password


# Employees can sign up and log in normally.
# The role is automatically set to 'employee' during registration.
# To create a manager, use the following command or from add user form:
# python manage.py createsuperuser 
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'employee'  
        if commit:
            user.save()
        return user



class LogInForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        label="Username"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label="Password"
    )


# Form to add user or manager by another manager
class AddUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password']




# Form to Change password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class ChangePasswordForm(forms.Form):
    """
    Form for changing the user's password.
    """
    old_password = forms.CharField(
        label="Old Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Old Password'})
    )
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'})
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'})
    )

    def __init__(self, user, *args, **kwargs):
        """
        Initialize the form with the current user.
        """
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_old_password(self):
        """
        Validate the old password.
        """
        old_password = self.cleaned_data.get("old_password")
        if not check_password(old_password, self.user.password):
            raise forms.ValidationError("The old password you entered is incorrect.")
        return old_password

    def clean_new_password1(self):
        """
        Validate the new password.
        """
        new_password1 = self.cleaned_data.get("new_password1")
        try:
            validate_password(new_password1, self.user)
        except ValidationError as e:
            raise forms.ValidationError(e.messages)
        return new_password1

    def clean(self):
        """
        Validate that the two new passwords match.
        """
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("The new passwords do not match.")

        return cleaned_data






# Form to edit user details
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "is_staff"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "is_staff": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
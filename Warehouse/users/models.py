# users/models.py
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db import models

    
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, role='employee', **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not password:
            raise ValueError('The Password field must be set')

        email = self.normalize_email(email)
        extra_fields.setdefault('is_staff', role == 'manager')  
        user = self.model(username=username, email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('role', 'manager')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    ROLE_CHOICES = [
        ('employee', 'Employee'),
        ('manager', 'Manager'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
    @property
    def is_employee(self):
        return self.role == 'employee'
    @property
    def is_manager(self):
        return self.role == 'manager'
    objects = UserManager() 


# who Try to sign up
class PendingUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  
    date_requested = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
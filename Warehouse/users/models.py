# users/models.py
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('employee', 'Employee'),
        ('manager', 'Manager'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')

    def is_employee(self):
        return self.role == 'employee'

    def is_manager(self):
        return self.role == 'manager'
    
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, role='employee', **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('role', 'manager')
        return self.create_user(username, email, password, **extra_fields)
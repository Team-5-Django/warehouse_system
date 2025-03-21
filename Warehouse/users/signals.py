from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PendingUser
from django.core.mail import send_mail

@receiver(post_save, sender=PendingUser)
def notify_admin_on_new_request(sender, instance, created, **kwargs):
    if created:
        send_mail(
            "New Account Request",
            f"A new user has requested an account:\n\nUsername: {instance.username}\nEmail: {instance.email}",
            "admin@example.com",  
            ["admin@example.com"],  
            fail_silently=False,
        )

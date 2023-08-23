from django.db import models
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.db.models.signals import post_save
from .models import Post
from datetime import date

@receiver(post_save, sender=Post)
def send_post_creation_notification(sender, instance, created, **kwargs):
    if created:
        subject = f'New Post Created ({date.today()})'
        message = f'A new post titled "{instance.title}" has been created.'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [instance.author.email]
        
        send_mail(subject, message, from_email, recipient_list)

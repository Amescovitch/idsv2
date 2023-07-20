from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Notification

@receiver(user_logged_in)
def send_welcome_notification(sender, user, request, **kwargs):
    message = "Bienvenue sur notre site !"
    notification = Notification(user=user, message=message)
    notification.save()

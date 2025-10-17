from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User




@receiver(post_save, sender=User)
def welcome_mail(sender,instance,created, **kwargs):
    if created:
        print("new user created")
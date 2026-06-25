from django.db.models.signals import post_save
from django.dispatch import receiver
from . models import *

@receiver(post_save, sender=User)
def cretae_profile(sender, created, instance, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    
from django.db.models.signals import post_save
from django.dispatch import receiver
# --- MODIFIED: Import the actual User model directly for clarity ---
from django.contrib.auth.models import User
from .models import Profile


# This is the only signal we need.
# It automatically creates a Profile whenever a new User is created.
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

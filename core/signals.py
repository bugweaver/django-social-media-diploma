from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from users.models import Profile


# Create profile when a new user is created
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()


post_save.connect(create_profile, sender=User)

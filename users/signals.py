'''
The reason we are using signals is to make sure that everytime a user is created,
a profile and profile image is set. So you don't have to go to the admin page and 
create those manually See 8th and 9th lines in apps.py too. That is also added
after creating signals
'''


from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
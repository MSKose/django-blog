from email.policy import default
from tkinter import CASCADE
from django.db import models
from PIL import Image

# see https://docs.djangoproject.com/en/4.1/ref/contrib/auth/ for User model
from django.contrib.auth.models import User


# we are creating Profile class since django, by default, does not have a field for 
# profile picture. Thus, we'll add it with this class using OneToOneField relation
class Profile(models.Model):

    # CASCADE: if the User is deleted, delete the Profile too. But not vice versa
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    
    # default: if the user does not pick up a image, default it to default.jpg I will provide
    # upload_to: the directory images will be uploaded to
    image = models.ImageField(default='default.jpg', upload_to='profile_pics') # with our MEDIA_ROOT set to media in settings.py, profile_pics directory will be created in media directory

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):   # this gets run after our model is saved. We want to add functionality to it
        super().save(*args, **kwargs)  # this already will run everytime an instance is saved. What we want to add is the follwing for pictures:

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

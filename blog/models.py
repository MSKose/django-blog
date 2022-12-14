from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    # since one post can one author but one author can have multiple posts we use many-to-1 relation
    # since we want to delete the posts related to the author if author is deleted, we use on_delete=models.CASCADE
    # but, notice that the opposite is not true; if a post is deleted author won't be deleted. It is called cascade for a reason
    author = models.ForeignKey(User, on_delete=models.CASCADE) 

    def __str__(self):
        return self.title
    
    def get_absolute_url(self): # without get_absolute_url function, we'd get an "No URL to redirect to" error. But, our post will still be created. This error is only about url redirection
        return reverse("post-detail", kwargs={"pk": self.pk})  # now, instead of redirect method we use reverse method to make the url redirection since we want full url 
    
from django.db import models
from  django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length = 500)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    updated = models.DateTimeField(auto_now = True)
    image = models.ImageField(upload_to = "media/img")
    created = models.DateTimeField(auto_now_add = True)

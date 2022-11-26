from email.policy import default
from telnetlib import STATUS
from django.db import models
from  django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from slugger import AutoSlugField
from taggit.managers import TaggableManager
from django.urls import reverse

# Create your models here.


STATUS = (
    (0, "Draft"),
    (1, "Publish")
)



class Section(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from= 'name',  unique=True, null=True)

    def __str__(self):
        return self.name




class Post(models.Model):
    title = models.CharField(max_length = 500)
    body = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    likes = models.ManyToManyField(User, default=None,  related_name="like")
    updated = models.DateTimeField(auto_now = True)
    image = models.ImageField(upload_to = "media/img")
    created = models.DateTimeField(auto_now_add = True)
    status = models.IntegerField(choices=STATUS, default=0)
    category = models.ForeignKey(Section, on_delete=models.CASCADE, blank=True, null=True)
    recommend = models.BooleanField(default=False)
    tags = TaggableManager()



    def like_count(self):
        return self.likes.all().count()

    def like(self, user):
        if user in self.likes.all():
          self.likes.remove(user)
        else:
          self.likes.add(user)
         
          
         
        self.save



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete= models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    body = RichTextUploadingField()
    created = models.DateTimeField(auto_now_add = True)

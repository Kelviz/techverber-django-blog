from django.shortcuts import render
from .models import Post

# Create your views here.

def HomePage(request):
    posts = Post.objects.all()

    return render(request, "post/home.html", {'posts':posts})



from audioop import reverse
import imp
from multiprocessing import context
from unicodedata import category
from django.views.generic import UpdateView, DeleteView, CreateView, DetailView
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect,  JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from taggit.models import Tag
from .models import Post, Comment, Section
from .forms import CommentModelForm, SignUpForm

# Create your views here.

def HomePage(request):
    posts = Post.objects.all()
    recommended = Post.objects.filter(recommend=True)
    paginator = Paginator(posts, 8)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request, "post/home.html", {'posts':posts, 'recommended':recommended})


def PostDetail(request, id):
    post = get_object_or_404(Post, id=id)
    tags = post.tags.similar_objects()[:5]
    comments = Comment.objects.filter(post=post)
    paginator = Paginator(comments, 3)
    page = request.GET.get('page')
    comments = paginator.get_page(page)

    form = CommentModelForm()
    if request.method == "POST":
        form = CommentModelForm(request.POST, request.FILES)
        if form.is_valid():
            body = form.cleaned_data['body']
            comment=Comment.objects.create(user=request.user, post=post, body=body)
            comment.save
            return redirect("content", id=id)
    
    context = {
        'post':post,
        'comments':comments,
        'form':form,
        'tags':tags

    }


    return render(request, "post/post_detail.html", context)



def Tagging(request, slug):
    tags = Tag.objects.filter(slug=slug).values_list('name', flat=True)
    posts = Post.objects.filter(tags__name__in=tags)
    paginator = Paginator(posts, 3)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    return render(request, 'post/tag.html', {'tags':tags, 'posts':posts})





@require_http_methods(["POST"])
def thumbs_rate(request):
    pk = request.POST.get('pk', None)
    user = request.user
    post =  Post.objects.get(pk=pk)
    

    try:
      post =  Post.objects.get(pk=pk)

    except Post.DoesNotExist:
        return HttpResponseBadRequest("Invalid message.")

    
    try:
        value = int(request.POST.get("value", None))

    except ValueError:
        return HttpResponseBadRequest("Value cannot be parsed to an integer.")

    if value > 0 :
        post.like(user)



    return JsonResponse({

        'pk': post.pk,
        'like': post.likes.count(),
        
    })



class UserRegisterView(CreateView):
    form_class = SignUpForm
    template_name = 'post/register.html'
    success_url = reverse_lazy('login')





def CategoryPage(request, slug):
    cats = Section.objects.all()
    posts = Post.objects.filter(category__slug=slug)
    paginator = Paginator(posts, 3)
    page = request.GET.get('page')
    posts = paginator.get_page(page)


    return render(request, 'post/section.html', {'posts':posts, 'cats':cats})



def Search(request):
    if request.method == "GET":
        searched = request.GET.get('search')
        posts = Post.objects.filter(title__icontains = searched)

        if posts:
            paginator = Paginator(posts, 3)
            page = request.GET.get('page')
            posts = paginator.get_page(page)

            return render(request, 'post/search.html', {'posts':posts, 'searched':searched})
        else:
            return render(request, 'post/search.html', {'posts':posts})
        

        





from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import PostForm  # Import form

def forum_home(request):
  posts = Post.objects.all().order_by('created_at')
  return render(request, 'forum_home.html', {'posts':posts})

def post_detail(request, slug):
  post = get_object_or_404(Post, slug=slug) #Fetch the post
  return render(request, 'post_detail.html', {'post': post})

#this is so convenient
@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

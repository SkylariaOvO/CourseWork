from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from .models import Post, Reply
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.db.models import Count
from django.shortcuts import render
from better_profanity import profanity
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


def apply_censorship(text):
    profanity.load_censor_words()
    return profanity.censor(text)
    
def forum_home(request):
    posts = Post.objects.annotate(
        popularity=Count("upvotes") - Count("downvotes")
    ).order_by("-popularity", "-created_at")  # Sort by popularity, then newest posts

    return render(request, "forum_home.html", {"posts": posts})

@login_required
def post_detail(request, slug):
    """Fetches the post and loads replies without altering structure."""
    post = get_object_or_404(Post, slug=slug)
    all_replies = post.replies.all().order_by("created_at") 

    return render(request, "post_detail.html", {"post": post, "all_replies": all_replies})

@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)  #Accepts file uploads
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.title = apply_censorship(post.title)#Censor title
            post.content = apply_censorship(post.content)
            post.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})


@login_required
def vote_post(request, slug, vote_type):
    """Handles upvoting/downvoting a post"""
    post = get_object_or_404(Post, slug=slug)

    if request.method == "POST":
        if vote_type == "upvote":
            if request.user in post.upvotes.all():
                post.upvotes.remove(request.user)
            else:
                post.upvotes.add(request.user)
                post.downvotes.remove(request.user)

        elif vote_type == "downvote":
            if request.user in post.downvotes.all():
                post.downvotes.remove(request.user)
            else:
                post.downvotes.add(request.user)
                post.upvotes.remove(request.user)

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))




@login_required
def reply_to_post(request, slug, parent_slug=None):
    """Handles both top-level replies and nested replies dynamically with attachments."""
    post = get_object_or_404(Post, slug=slug)
    parent_reply = get_object_or_404(Reply, slug=parent_slug) if parent_slug else None 

    if request.method == "POST":
        content = request.POST.get("content")
        file = request.FILES.get("file")  # Handle file uploads

        if content:
            new_reply = Reply.objects.create(
                post=post, 
                author=request.user, 
                content=apply_censorship(content),
                parent=parent_reply,
                file=file
            )

            if request.headers.get('HX-Request'):
                html = render_to_string("reply_partial.html", {"reply": new_reply, "children": []})
                return HttpResponse(html)

    return HttpResponseRedirect(reverse("post_detail", args=[post.slug]))


def reply_form(request, slug, parent_slug):
    """Renders the reply form dynamically when a user clicks 'Reply'."""
    post = get_object_or_404(Post, slug=slug)
    parent_reply = get_object_or_404(Reply, slug=parent_slug)

    if request.headers.get('HX-Request'):
        return render(request, "reply_form.html", {"post": post, "parent_reply": parent_reply})

    return HttpResponseRedirect(reverse("post_detail", args=[post.slug]))

@login_required
def delete_reply(request, slug):
    """Allows users to delete their own replies and admins to delete any reply."""
    reply = get_object_or_404(Reply, slug=slug)

    if request.user == reply.author or request.user.is_staff:
        reply.delete()
        return HttpResponse(status=204)

    return HttpResponse(status=403)

@login_required
def edit_post(request, slug):
    """Allows users to edit their own posts."""
    post = get_object_or_404(Post, slug=slug)

    if request.user != post.author:
        return HttpResponse(status=403)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.title = apply_censorship(post.title)
            post.content = apply_censorship(post.content)
            post.save()
            return redirect(reverse('dashboard:my_posts'))

    else:
        form = PostForm(instance=post)

    return render(request, 'edit_post.html', {'form': form, 'post': post})




@csrf_exempt
@login_required
def delete_post(request, slug):
    """Allows users to delete their own posts and refresh the page after deletion."""
    post = get_object_or_404(Post, slug=slug)

    if request.user == post.author:
        post.delete()
        return HttpResponseRedirect(reverse("dashboard:my_posts"))

    return HttpResponse(status=403)

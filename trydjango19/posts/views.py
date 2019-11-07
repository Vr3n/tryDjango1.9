from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post
from .forms import PostForm

# Create your views here.


def posts_home(request):
    queryset = Post.objects.all()
    context = {
        "object_list": queryset,
        "title": "Home"
    }
    return render(request, "index.html", context)


def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        print(form.cleaned_data.get('title'))
        instance.save()
        messages.success(request, "Post successfully Created.")
        return HttpResponseRedirect(instance.get_absolute_url())
    # if request.method == "POST":
    #     # Can be done like this
    #     # title = request.POST.get('title')
    #     # Post.objects.create(title=title)

    context = {
        "form": form,
        "title": "Create Post"
    }
    return render(request, "post_form.html", context)


def post_detail(request, id=None):
    # instance = Post.objects.get(id=1)
    instance = get_object_or_404(Post, id=id)
    context = {
        "instance": instance,
        "title": "Detail",
    }

    return render(request, "post_detail.html", context)


def post_list(request):
    # if request.user.is_authenticated():
    #     context = {
    #         "title": "My user List"
    #     }
    # else:
    queryset = Post.objects.all().order_by('-timestamp')
    context = {
        "object_list": queryset,
    }
    return render(request, "index.html", context)


def post_update(request, id=None):
    instance = get_object_or_404(Post, id=id)

    form = PostForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        print(form.cleaned_data.get('title'))
        instance.save()
        messages.success(request, "Post successfully Updated.")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "instance": instance,
        "title": "Update",
        "form": form,
    }

    return render(request, "post_update_form.html", context)


def post_delete(request, id=None):
    instance = get_object_or_404(Post, id=id)

    form = PostForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.delete()
        messages.success(request, "Post successfully deleted.")
        return redirect('posts:post-list')

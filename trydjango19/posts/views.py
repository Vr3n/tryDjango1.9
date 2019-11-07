from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from .models import Post
from .forms import PostForm

# Create your views here.


def posts_home(request):
    queryset_list = Post.objects.all()

    # Pagination
    paginator = Paginator(queryset_list, 2)
    page_request_var = "posts"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an Integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        "object_list": queryset,
        "page_request_var": page_request_var,
        "title": "Home"
    }
    return render(request, "index.html", context)


def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
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


def post_detail(request, slug=None):
    # instance = Post.objects.get(slug=1)
    instance = get_object_or_404(Post, slug=slug)
    context = {
        "instance": instance,
        "title": "Detail",
    }

    return render(request, "post_detail.html", context)


def post_list(request):
    queryset = Post.objects.all().order_by('-timestamp')

    # Pagination
    paginator = Paginator(queryset, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an Integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    context = {
        "object_list": queryset,
    }

    return render(request, "post_list.html", context)


def post_update(request, id=None):
    instance = get_object_or_404(Post, id=id)

    form = PostForm(request.POST or None,
                    request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        print(form.cleaned_data.get('title'))
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

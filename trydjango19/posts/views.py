from django.db.models import Q
from django.utils import timezone
from urllib.parse import quote_plus
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.contrib.contenttypes.models import ContentType

from .models import Post
from .forms import PostForm
from comments.forms import CommentForm
from comments.models import Comment, CommentManager

# Create your views here.


def posts_home(request):
    today = timezone.now().date()
    queryset_list = Post.objects.active()

    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()

    # Search Query.
    query = request.GET.get('q')
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()

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
        "title": "Home",
        "today": today
    }
    return render(request, "index.html", context)


def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
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

    if instance.draft or instance.publish > timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404

    share_string = quote_plus(instance.content)

    intitial_data = {
        "content_type": instance.get_content_type,
        "object_id": instance.id
    }
    comment_form = CommentForm(request.POST or None, initial=intitial_data)
    if comment_form.is_valid():
        c_type = comment_form.cleaned_data.get('content_type')
        content_type = ContentType.objects.get(model=c_type)
        obj_id = comment_form.cleaned_data.get('object_id')
        content_data = comment_form.cleaned_data.get('content')
        new_comment, created = Comment.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=obj_id,
            content=content_data
        )

    comments = instance.comments

    context = {
        "instance": instance,
        "title": "Detail",
        "share_string": share_string,
        "comment_form": comment_form,
        "comments": comments,
    }

    return render(request, "post_detail.html", context)


def post_list(request):
    queryset_list = Post.objects.active()

    # Pagination
    paginator = Paginator(queryset_list, 5)
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
        "object_list": queryset_list,
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

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def posts_home(request):
    context = {
        "title": "Home"
    }
    return render(request, "index.html", context)


def post_create(request):
    context = {
        "title": "Create Post"
    }
    return render(request, "create.html", context)


def post_detail(request):
    return HttpResponse("<h1>Detail</h1>")


def post_list(request):
    # if request.user.is_authenticated():
    #     context = {
    #         "title": "My user List"
    #     }
    # else:
    context = {
        "title": "List"
    }
    return render(request, "list.html", context)


def post_update(request):
    return HttpResponse("<h1>Update</h1>")


def post_delete(request):
    return HttpResponse("<h1>Delete</h1>")

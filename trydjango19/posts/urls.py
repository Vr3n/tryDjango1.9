from django.conf.urls import url
from .views import (posts_home,
                    post_create,
                    post_delete,
                    post_detail,
                    post_list,
                    post_update
                    )

# Write your URL patterns here.
urlpatterns = [
    url(r'^$',  posts_home, name="home"),
    url(r'^create', post_create, name="post-create"),
    url(r'^delete/(?P<id>\d+)/$', post_delete, name="post-delete"),
    url(r'^(?P<slug>[\w-]+)/$', post_detail, name="post-detail"),
    url(r'^list', post_list, name="post-list"),
    url(r'^(?P<id>\d+)/edit/$', post_update, name="post-update"),
]

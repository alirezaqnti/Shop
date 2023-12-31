from django.urls import path
from . import views

urlpatterns = [
    path("", views.PostsList.as_view(), name="PostsList"),
    path("posts/getposts/", views.GetPosts.as_view(), name="GetPosts"),
    path("post/<str:RPO>", views.PostDetail.as_view(), name="PostDetail"),
]

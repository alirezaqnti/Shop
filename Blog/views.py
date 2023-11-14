from rest_framework.generics import ListAPIView
from django.views.generic import TemplateView, ListView
from .models import Post, PostComment, PostRate, PostTags
from .serializers import PostSerializer
from django.core.paginator import Paginator
from rest_framework.pagination import LimitOffsetPagination
from django.shortcuts import redirect
from django.db.models import Q, Avg


class PostsList(TemplateView):
    template_name = "Main/blog.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Lt = Post.objects.filter(Active=True).order_by("-Created_At")[:3]
        Tg = PostTags.objects.all().order_by("-Usage")[:10]
        context["Late"] = Lt
        context["Tags"] = Tg
        return context


class GetPosts(ListAPIView):
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        PS = Post.objects.filter(Active=True).order_by("-Created_At")
        kwargs = self.request.GET
        txt = kwargs.get("txt")
        tag = kwargs.get("tag")
        print("PS:", PS)

        if txt:
            PS = PS.filter(Q(Title__contains=txt) | Q(Text__contains=txt))
        print("PS:", PS)

        return PS


class PostDetail(TemplateView):
    template_name = "Main/blog-details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = kwargs["slug"]
        Ps = (
            Post.objects.filter(Slug=slug)
            .prefetch_related("tag_post", "comment_post", "rate_post")
            .first()
        )
        Nx = Post.objects.filter(Created_At__gte=Ps.Created_At).exclude(Slug=slug).first()
        print(Nx)
        Pv = Post.objects.filter(Created_At__lte=Ps.Created_At).exclude(Slug=slug).first()
        print(Pv)
        Lt = Post.objects.filter(Active=True).exclude(Slug=slug).order_by("-Created_At")[:3]
        context["Post"] = Ps
        context["Late"] = Lt
        context["Next"] = Nx
        context["Prev"] = Pv
        return context

    def post(self, request, *args, **kwargs):
        slug = kwargs["slug"]
        Ps = Post.objects.get(Slug=slug)
        Cm = PostComment()
        Cm.Post = Ps
        Cm.Name = request.POST["Name"]
        Cm.Phone = request.POST["Phone"]
        Cm.Text = request.POST["Text"]
        Cm.Rate = request.POST["Rate"]
        Cm.save()
        avg = PostComment.objects.aggregate(Avg("Rate"))
        print("AVG:", avg["Rate__avg"])
        Ps.Rate = avg["Rate__avg"]
        Ps.save()
        return redirect("PostDetail", slug)

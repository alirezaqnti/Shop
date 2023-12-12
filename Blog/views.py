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
        Ps = Post.objects.filter(Active=True).order_by("-Created_At")[:3]
        Tg = PostTags.objects.all().order_by("-Usage")[:10]
        RT = Post.objects.filter(Active=True).order_by("-Rate")[:3]
        TGs = PostTags.objects.all().order_by("-ClickCount")[:10]
        context["Posts"] = Ps
        context["Tags"] = Tg
        context["Fav_Post"] = RT
        context["Fav_Tags"] = TGs
        return context


class GetPosts(ListAPIView):
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        PS = Post.objects.filter(Active=True).order_by("-Created_At")
        kwargs = self.request.GET
        txt = kwargs.get("txt")
        tag = kwargs.get("tag")

        if txt:
            PS = PS.filter(Q(Title__contains=txt) | Q(Text__contains=txt))

        return PS


class PostDetail(TemplateView):
    template_name = "Main/blog-details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        RPO = kwargs["RPO"]
        Ps = (
            Post.objects.filter(RPO=RPO)
            .prefetch_related("tag_post", "comment_post", "rate_post")
            .first()
        )
        Lt = (
            Post.objects.filter(Active=True)
            .exclude(RPO=RPO)
            .order_by("-Created_At")[:5]
        )
        RT = Post.objects.filter(Active=True).exclude(RPO=RPO).order_by("-Rate")[:3]
        TGs = PostTags.objects.all().order_by("-ClickCount")[:10]
        context["Post"] = Ps
        context["Late"] = Lt
        context["Fav_Post"] = RT
        context["Fav_Tags"] = TGs
        context["Tags"] = Ps.tag_post.all()
        context["CMs"] = Ps.comment_post.all()
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
        Ps.Rate = avg["Rate__avg"]
        Ps.save()
        return redirect("PostDetail", slug)

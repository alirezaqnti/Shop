from django.views.static import serve
from . import settings
from django.contrib import admin
from django.urls import path, re_path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("Main.urls")),
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    path("__debug__/", include("debug_toolbar.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("users/", include("Users.urls")),
    path("warehouse/", include("Warehouse.urls")),
    path("products/", include("Products.urls")),
    path("blog/", include("Blog.urls")),
]

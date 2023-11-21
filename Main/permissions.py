from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import redirect
from Main.context_processors import getActiveUser


class IsUserLoggedIn(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        usr = getActiveUser(request)
        if usr != "":
            return super().dispatch(request, *args, **kwargs)
        else:
            return JsonResponse(
                {"stat": 500, "report": "ابتدا وارد حساب کاربری خود شوید"}
            )

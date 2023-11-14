from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import redirect


class IsUserLoggedIn(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        super().dispatch(request, *args, **kwargs)
        try:
            print('USER:: ',request.session["User_id"])
            return super().dispatch(request, *args, **kwargs)
        except:
            return JsonResponse({"stat": 301})

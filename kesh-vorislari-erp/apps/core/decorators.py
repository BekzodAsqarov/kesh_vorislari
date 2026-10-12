from collections.abc import Callable
from functools import wraps

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect


def role_required(*roles: str, allow_admin: bool = True) -> Callable:
    """Restrict a Django view to one or more user roles."""

    def decorator(view_func: Callable) -> Callable:
        @wraps(view_func)
        def _wrapped(request: HttpRequest, *args, **kwargs) -> HttpResponse:
            user = request.user
            if not user.is_authenticated:
                return redirect("accounts:login")
            if allow_admin and user.is_admin:
                return view_func(request, *args, **kwargs)
            if user.role in roles:
                return view_func(request, *args, **kwargs)
            messages.error(request, "You do not have permission to access this page.")
            return redirect("dashboard:index")

        return _wrapped

    return decorator

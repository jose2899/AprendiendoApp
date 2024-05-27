from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from functools import wraps
from django.urls import reverse


def permission_required_custom(perm, login_url=None, raise_exception=False):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.has_perm(perm):
                return view_func(request, *args, **kwargs)
            else:
                if raise_exception:
                    raise PermissionDenied
                else:
                    # Redirigir a la página actual
                    return redirect(request.META.get('HTTP_REFERER', reverse('index')))
        return _wrapped_view
    return decorator
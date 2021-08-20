from django.shortcuts import redirect
from django.urls import reverse


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return redirect(reverse('yumminess:dashboard'))

    return wrapper_func

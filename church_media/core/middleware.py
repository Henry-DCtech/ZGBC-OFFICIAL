from django.shortcuts import redirect
from django.conf import settings
from django.urls import resolve, Resolver404

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            return self.get_response(request)

        exempt_paths = ['/login/', '/logout/', '/password-reset/', '/', '/admin/']
        if any(request.path_info.startswith(path) for path in exempt_paths):
            return self.get_response(request)

        try:
            resolved = resolve(request.path_info)
            if resolved.url_name == 'password_reset_confirm':
                return self.get_response(request)
        except Resolver404:
            pass

        return redirect(settings.LOGIN_URL)
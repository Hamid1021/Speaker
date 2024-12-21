from django.http import HttpResponseForbidden

class RedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'redirected' not in request.session and request.path in ['/success/', '/faill/']:
            return HttpResponseForbidden("دسترسی شما محدود شده است")
        response = self.get_response(request)
        return response


from django.shortcuts import redirect
from django.urls import reverse

class CustomLoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and request.path.startswith('/admin/'):
            return redirect(reverse("account:login") + '?next=' + reverse("application:assign"))
        response = self.get_response(request)
        return response

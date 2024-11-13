from django.http import HttpResponseForbidden

class RedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'redirected' not in request.session and request.path in ['/success/', '/faill/']:
            return HttpResponseForbidden("دسترسی شما محدود شده است")
        response = self.get_response(request)
        return response

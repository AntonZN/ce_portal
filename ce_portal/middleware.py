from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin


class AuthRequiredMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            path = request.path_info
            if path != settings.LOGIN_URL and path.find("api") == -1:
                return HttpResponseRedirect(settings.LOGIN_URL)

from django.utils.deprecation import MiddlewareMixin

from ipware import get_client_ip


class RealIPMiddleware(MiddlewareMixin):
    """
    Django middleware to get real ip from request, and set to META
    Usage:
        1. Add `ipware.middleware.RealIPMiddleware` to MIDDLEWARE,
        2. Get real ip from request.META['IPWARE_REAL_IP']
    """

    def process_request(self, request):
        real_ip, _ = get_client_ip(request)
        request.META['IPWARE_REAL_IP'] = real_ip
        return None

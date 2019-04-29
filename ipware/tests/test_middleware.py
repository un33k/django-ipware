from django.conf import settings
from django.http import HttpRequest
from django.test import TestCase

from ipware.middleware import RealIPMiddleware


class MiddlewareTestCase(TestCase):

    def setUp(self):
        self.request = HttpRequest()
        self.request.META = {
            'HTTP_X_FORWARDED_FOR': '8.8.8.8, 192.168.1.1',
        }

    def test_real_ip_middleware(self):
        middleware = RealIPMiddleware()
        settings.IPWARE_PROXY_COUNT = 1
        response = middleware.process_request(self.request)
        self.assertIsNone(response)
        self.assertEqual(self.request.META['IPWARE_REAL_IP'], '8.8.8.8')

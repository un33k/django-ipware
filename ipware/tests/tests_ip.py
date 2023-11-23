# -*- coding: utf-8 -*-

from django.http import HttpRequest
from django.test import TestCase

from ipware import get_client_ip


class IpTestCase(TestCase):
    """IP address Test"""

    # run one test, to ensure we are loading python ipware correctly
    # python-ipware has all the tests, so we don't need to test it here
    def test_load(self):
        request = HttpRequest()
        request.META = {
            'HTTP_X_FORWARDED_FOR': '177.139.233.139, 198.84.193.157, 198.84.193.158',
        }
        result = get_client_ip(request)
        self.assertEqual(result, ("177.139.233.139", True))

    def test_meta_proxy_order_left_most(self):
        request = HttpRequest()
        request.META = {
            'HTTP_X_FORWARDED_FOR': '177.139.233.139, 198.84.193.157, 198.84.193.158',
        }
        result = get_client_ip(request, proxy_order='left-most')
        self.assertEqual(result, ("177.139.233.139", True))

    def test_meta_singleton_proxy_count(self):
        request = HttpRequest()
        request.META = {
            'HTTP_X_FORWARDED_FOR': '177.139.233.139, 198.84.193.157, 198.84.193.158',
        }
        result = get_client_ip(request, proxy_count=2)
        self.assertEqual(result, ("177.139.233.139", True))

    def test_meta_proxy_trusted_ips_exact_ip_check(self):
        request = HttpRequest()
        request.META = {
            'HTTP_X_FORWARDED_FOR': '177.139.233.139, 198.84.193.157, 198.84.193.158',
        }
        result = get_client_ip(request, proxy_trusted_ips=['198.84.193.157', '198.84.193.158'])
        self.assertEqual(result, ("177.139.233.139", True))

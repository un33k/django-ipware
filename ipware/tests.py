# -*- coding: utf-8 -*-

from django.http import HttpRequest
from django.test import TestCase
from ipware.ip import get_ip_address_from_request

class IPTestCase(TestCase):
    """IP address Test"""

    def test_x_forwarded_for_multiple(self):
        request = HttpRequest()
        request.META = {
            'HTTP_X_FORWARDED_FOR': '192.168.255.182, 10.0.0.0, 127.0.0.1, 198.84.193.157, 177.139.233.139',
            'HTTP_X_REAL_IP': '177.139.233.132',
            'REMOTE_ADDR': '177.139.233.133',
        }
        ip = get_ip_address_from_request(request)
        self.assertEquals(ip, "198.84.193.157")

    def test_x_forwarded_for_multiple_bad_address(self):
        request = HttpRequest()
        request.META = {
            'HTTP_X_FORWARDED_FOR': 'unknown, 192.168.255.182, 10.0.0.0, 127.0.0.1, 198.84.193.157, 177.139.233.139',
            'HTTP_X_REAL_IP': '177.139.233.132',
            'REMOTE_ADDR': '177.139.233.133',
        }
        ip = get_ip_address_from_request(request)
        self.assertEquals(ip, "198.84.193.157")

    def test_x_forwarded_for_singleton(self):
        request = HttpRequest()
        request.META = {
            'HTTP_X_FORWARDED_FOR': '177.139.233.139',
            'HTTP_X_REAL_IP': '177.139.233.132',
            'REMOTE_ADDR': '177.139.233.133',
        }
        ip = get_ip_address_from_request(request)
        self.assertEquals(ip, "177.139.233.139")

    def test_x_forwarded_for_singleton_private_address(self):
        request = HttpRequest()
        request.META = {
            'HTTP_X_FORWARDED_FOR': '192.168.255.182',
            'HTTP_X_REAL_IP': '177.139.233.132',
            'REMOTE_ADDR': '177.139.233.133',
        }
        ip = get_ip_address_from_request(request)
        self.assertEquals(ip, "177.139.233.132")

    def test_bad_x_forwarded_for_fallback_on_x_real_ip(self):
        request = HttpRequest()
        request.META = {
            'HTTP_X_FORWARDED_FOR': 'unknown 177.139.233.139',
            'HTTP_X_REAL_IP': '177.139.233.132',
            'REMOTE_ADDR': '177.139.233.133',
        }
        ip = get_ip_address_from_request(request)
        self.assertEquals(ip, "177.139.233.132")

    def test_empty_x_forwarded_for_fallback_on_x_real_ip(self):
        request = HttpRequest()
        request.META = {
            'HTTP_X_FORWARDED_FOR': '',
            'HTTP_X_REAL_IP': '177.139.233.132',
            'REMOTE_ADDR': '177.139.233.133',
        }
        ip = get_ip_address_from_request(request)
        self.assertEquals(ip, "177.139.233.132")

    def test_empty_x_forwarded_for_empty_x_real_ip_fallback_on_remote_addr(self):
        request = HttpRequest()
        request.META = {
            'HTTP_X_FORWARDED_FOR': '',
            'HTTP_X_REAL_IP': '177.139.233.132',
            'REMOTE_ADDR': '177.139.233.133',
        }
        ip = get_ip_address_from_request(request)
        self.assertEquals(ip, "177.139.233.132")

    def test_empty_x_forwarded_for_private_x_real_ip_fallback_on_remote_addr(self):
        request = HttpRequest()
        request.META = {
            'HTTP_X_FORWARDED_FOR': '',
            'HTTP_X_REAL_IP': '192.168.255.182',
            'REMOTE_ADDR': '177.139.233.133',
        }
        ip = get_ip_address_from_request(request)
        self.assertEquals(ip, "177.139.233.133")

    def test_remote_addr_fallback(self):
        request = HttpRequest()
        request.META = {
            'HTTP_X_FORWARDED_FOR': '',
            'HTTP_X_REAL_IP': '',
            'REMOTE_ADDR': '177.139.233.133',
        }
        ip = get_ip_address_from_request(request)
        self.assertEquals(ip, "177.139.233.133")




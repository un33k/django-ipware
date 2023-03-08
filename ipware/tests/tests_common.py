# -*- coding: utf-8 -*-

from django.http import HttpRequest
from django.test import TestCase

from .. import utils as util


class IPv4TestCase(TestCase):
    """IP address Test"""


    def test_is_valid_ip(self):
        ip = '177.139.233.139'
        assert util.is_valid_ip(ip)

        ip = '3ffe:1900:4545:3:200:f8ff:fe21:67cf'
        assert util.is_valid_ip(ip)

    def test_is_invalid_ip(self):
        ip = '177.139.233.139x'
        assert not util.is_valid_ip(ip)

        ip = '3ffe:1900:4545:3:200:f8ff:fe21:67cz'
        assert not util.is_valid_ip(ip)

    def test_is_private_ip(self):
        ip = '127.0.0.1'
        assert util.is_private_ip(ip)

        ip = '::1/128'
        assert util.is_private_ip(ip)

    def test_is_public_ip(self):
        ip = '177.139.233.139'
        assert util.is_public_ip(ip)

        ip = '74dc::02ba'
        assert util.is_public_ip(ip)

    def test_is_loopback_ip(self):
        ip = '127.0.0.1'
        assert util.is_loopback_ip(ip)

        ip = '177.139.233.139'
        assert not util.is_loopback_ip(ip)

        ip = '10.0.0.1'
        assert not util.is_loopback_ip(ip)

        ip = '::1/128'
        assert util.is_loopback_ip(ip)

        ip = '74dc::02ba'
        assert not util.is_loopback_ip(ip)

        ip = '2001:db8:'
        assert not util.is_loopback_ip(ip)

    def test_http_request_meta_headers(self):
        request = HttpRequest()
        ip_str = '192.168.255.182, 10.0.0.0, 127.0.0.1, 198.84.193.157, 177.139.233.139,'
        request.META = { 'HTTP_X_FORWARDED_FOR': ip_str }
        value = util.get_request_meta(request, 'HTTP_X_FORWARDED_FOR')
        assert value == ip_str

    def test_ips_from_strings(self):
        ip_str = '192.168.255.182, 198.84.193.157, 177.139.233.139 ,'
        result = util.get_ips_from_string(ip_str)
        assert result == (['192.168.255.182', '198.84.193.157', '177.139.233.139'], 3)

    def test_get_ip_info(self):
        ip = '127.0.0.1'
        result = util.get_ip_info(ip)
        assert result, (ip, False)

        ip = '10.0.01'
        result = util.get_ip_info(ip)
        assert result, (ip, False)

        ip = '74dc::02ba'
        result = util.get_ip_info(ip)
        assert result, (ip, True)

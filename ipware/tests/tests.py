# -*- coding: utf-8 -*-
import logging
import sys
from abc import ABC
from ipaddress import ip_address

from django.http import HttpRequest
from django.test import TestCase
from ipware import get_client_ip
from .. import defaults
from ..descriptor import Header, ReverseProxy, Order


class AbstractTestCase():
    def test_meta_single(self):
        request = HttpRequest()
        request.META = {'REMOTE_ADDR': self.REMOTE_ADDR}
        request.headers = {
            'X-FORWARDED-for': self.FORWARDED_HEADER,
        }
        with self.settings(IPWARE_REVERSE_PROXIES=[]):
            result = get_client_ip(request)
        self.assertEqual(result, ip_address(self.REMOTE_ADDR))

    def test_meta_multi_exact(self):
        request = HttpRequest()
        request.META = {
            'REMOTE_ADDR': self.REMOTE_ADDR,
        }
        request.headers = {
            'X-FORWARDED-for': self.FORWARDED_HEADER,
        }
        with self.settings(IPWARE_REVERSE_PROXIES=[
            ReverseProxy(Header("X-Forwarded-For"), self.REMOTE_ADDR, self.FORWARDED_ITEM_2, self.FORWARDED_ITEM_3)]):
            result = get_client_ip(request)
        self.assertEqual(result, ip_address(self.FORWARDED_ITEM_1))

    def test_meta_multi_from_proxy_itself(self):
        request = HttpRequest()
        request.META = {
            'REMOTE_ADDR': self.REMOTE_ADDR,
        }
        request.headers = {
            'X-FORWARDED-for': self.FORWARDED_HEADER,
        }
        with self.settings(IPWARE_REVERSE_PROXIES=[
            ReverseProxy(Header("X-Forwarded-For"), self.REMOTE_ADDR, self.FORWARDED_ITEM_1, self.FORWARDED_ITEM_2,
                         self.FORWARDED_ITEM_3)]):
            result = get_client_ip(request)
        self.assertEqual(result, ip_address(self.FORWARDED_ITEM_1))

    def test_meta_multi_with_unknown_headers(self):
        request = HttpRequest()
        request.META = {
            'REMOTE_ADDR': self.REMOTE_ADDR,
        }
        request.headers = {
            'X-FORWARDED-for': self.FORWARDED_HEADER,
        }
        with self.settings(IPWARE_REVERSE_PROXIES=[ReverseProxy(Header("X-Forwarded-For"), self.REMOTE_ADDR)]):
            result = get_client_ip(request)
        self.assertEqual(result, ip_address(self.FORWARDED_ITEM_3))

    def test_meta_proxy_order_left_most(self):
        request = HttpRequest()
        request.META = {
            'REMOTE_ADDR': self.REMOTE_ADDR,
        }
        request.headers = {
            'X-FORWARDED-for': self.FORWARDED_HEADER,
        }
        with self.settings(IPWARE_REVERSE_PROXIES=[
            ReverseProxy(Header("X-Forwarded-For", order=Order.HEADER_PREPENDED), self.REMOTE_ADDR)]):
            result = get_client_ip(request)
        self.assertEqual(result, ip_address(self.FORWARDED_ITEM_1))

    def test_meta_proxy_order_right_most(self):
        request = HttpRequest()
        request.META = {
            'REMOTE_ADDR': self.REMOTE_ADDR,
        }
        request.headers = {
            'X-FORWARDED-for': self.FORWARDED_HEADER,
        }
        with self.settings(IPWARE_REVERSE_PROXIES=[
            ReverseProxy(Header("X-Forwarded-For", order=Order.HEADER_APPENDED), self.REMOTE_ADDR)]):
            result = get_client_ip(request)
        self.assertEqual(result, ip_address(self.FORWARDED_ITEM_3))

    def test_meta_proxy_ignore_parsing_error(self):
        request = HttpRequest()
        request.META = {
            'REMOTE_ADDR': self.REMOTE_ADDR,
        }
        request.headers = {
            'X-FORWARDED-for': self.FORWARDED_HEADER_BOGUS,
        }
        with self.settings(IPWARE_REVERSE_PROXIES=[ReverseProxy(Header("X-Forwarded-For"), self.REMOTE_ADDR)]):
            result = get_client_ip(request)
        self.assertEqual(result, ip_address(self.FORWARDED_ITEM_3))

    def test_meta_proxy_parsing_error(self):
        request = HttpRequest()
        request.META = {
            'REMOTE_ADDR': self.REMOTE_ADDR,
        }
        request.headers = {
            'X-FORWARDED-for': self.FORWARDED_HEADER_UNKNOWN,
        }
        with self.settings(IPWARE_REVERSE_PROXIES=[ReverseProxy(Header("X-Forwarded-For"), self.REMOTE_ADDR)]):
            with self.assertRaises(Exception):
                result = get_client_ip(request)

    def tearDown(self) -> None:
        self.databases_handle.__exit__(None, None, None)

    def setUp(self) -> None:
        self.databases_handle = self.settings(DATABASES=[])
        self.databases_handle.__enter__()

        self.FORWARDED_HEADER_BOGUS = ""
        self.FORWARDED_HEADER_UNKNOWN = ""
        self.REMOTE_ADDR = ""
        self.FORWARDED_ITEM_1 = ""
        self.FORWARDED_ITEM_2 = ""
        self.FORWARDED_ITEM_3 = ""
        self.FORWARDED_HEADER = ""


class IPv4TestCase(AbstractTestCase, TestCase):
    """IP address Test"""

    def test_meta_single(self):
        request = HttpRequest()
        request.META = {'REMOTE_ADDR': self.REMOTE_ADDR}
        request.headers = {
            'X-FORWARDED-for': self.FORWARDED_HEADER,
        }
        with self.settings(IPWARE_REVERSE_PROXIES=[]):
            result = get_client_ip(request)
        self.assertEqual(result, ip_address(self.REMOTE_ADDR))

    def test_meta_multi_exact(self):
        request = HttpRequest()
        request.META = {
            'REMOTE_ADDR': self.REMOTE_ADDR,
        }
        request.headers = {
            'X-FORWARDED-for': self.FORWARDED_HEADER,
        }
        with self.settings(IPWARE_REVERSE_PROXIES=[
            ReverseProxy(Header("X-Forwarded-For"), self.REMOTE_ADDR, self.FORWARDED_ITEM_2, self.FORWARDED_ITEM_3)]):
            result = get_client_ip(request)
        self.assertEqual(result, ip_address(self.FORWARDED_ITEM_1))

    def test_meta_multi_from_proxy_itself(self):
        request = HttpRequest()
        request.META = {
            'REMOTE_ADDR': self.REMOTE_ADDR,
        }
        request.headers = {
            'X-FORWARDED-for': self.FORWARDED_HEADER,
        }
        with self.settings(IPWARE_REVERSE_PROXIES=[
            ReverseProxy(Header("X-Forwarded-For"), self.REMOTE_ADDR, self.FORWARDED_ITEM_1, self.FORWARDED_ITEM_2,
                         self.FORWARDED_ITEM_3)]):
            result = get_client_ip(request)
        self.assertEqual(result, ip_address(self.FORWARDED_ITEM_1))

    def test_meta_multi_with_unknown_headers(self):
        request = HttpRequest()
        request.META = {
            'REMOTE_ADDR': self.REMOTE_ADDR,
        }
        request.headers = {
            'X-FORWARDED-for': self.FORWARDED_HEADER,
        }
        with self.settings(IPWARE_REVERSE_PROXIES=[ReverseProxy(Header("X-Forwarded-For"), self.REMOTE_ADDR)]):
            result = get_client_ip(request)
        self.assertEqual(result, ip_address(self.FORWARDED_ITEM_3))

    def test_meta_proxy_order_left_most(self):
        request = HttpRequest()
        request.META = {
            'REMOTE_ADDR': self.REMOTE_ADDR,
        }
        request.headers = {
            'X-FORWARDED-for': self.FORWARDED_HEADER,
        }
        with self.settings(IPWARE_REVERSE_PROXIES=[
            ReverseProxy(Header("X-Forwarded-For", order=Order.HEADER_PREPENDED), self.REMOTE_ADDR)]):
            result = get_client_ip(request)
        self.assertEqual(result, ip_address(self.FORWARDED_ITEM_1))

    def test_meta_proxy_order_right_most(self):
        request = HttpRequest()
        request.META = {
            'REMOTE_ADDR': self.REMOTE_ADDR,
        }
        request.headers = {
            'X-FORWARDED-for': self.FORWARDED_HEADER,
        }
        with self.settings(IPWARE_REVERSE_PROXIES=[
            ReverseProxy(Header("X-Forwarded-For", order=Order.HEADER_APPENDED), self.REMOTE_ADDR)]):
            result = get_client_ip(request)
        self.assertEqual(result, ip_address(self.FORWARDED_ITEM_3))

    def test_meta_proxy_ignore_parsing_error(self):
        request = HttpRequest()
        request.META = {
            'REMOTE_ADDR': self.REMOTE_ADDR,
        }
        request.headers = {
            'X-FORWARDED-for': self.FORWARDED_HEADER_BOGUS,
        }
        with self.settings(IPWARE_REVERSE_PROXIES=[ReverseProxy(Header("X-Forwarded-For"), self.REMOTE_ADDR)]):
            result = get_client_ip(request)
        self.assertEqual(result, ip_address(self.FORWARDED_ITEM_3))

    def test_meta_proxy_parsing_error(self):
        request = HttpRequest()
        request.META = {
            'REMOTE_ADDR': self.REMOTE_ADDR,
        }
        request.headers = {
            'X-FORWARDED-for': self.FORWARDED_HEADER_UNKNOWN,
        }
        with self.settings(IPWARE_REVERSE_PROXIES=[ReverseProxy(Header("X-Forwarded-For"), self.REMOTE_ADDR)]):
            with self.assertRaises(Exception):
                result = get_client_ip(request)

    def tearDown(self) -> None:
        self.databases_handle.__exit__(None, None, None)

    def setUp(self) -> None:
        self.databases_handle = self.settings(DATABASES=[])
        self.databases_handle.__enter__()
        self.FORWARDED_HEADER_BOGUS = 'unknown,foo,,bar,,,, 198.84.193.157, 198.84.193.158'
        self.FORWARDED_HEADER_UNKNOWN = '177.139.233.139, 198.84.193.157, unknown'
        self.REMOTE_ADDR = '177.139.233.133'
        self.FORWARDED_ITEM_1 = '177.139.233.139'
        self.FORWARDED_ITEM_2 = '198.84.193.157'
        self.FORWARDED_ITEM_3 = '198.84.193.158'
        self.FORWARDED_HEADER = '177.139.233.139, 198.84.193.157, 198.84.193.158'


class IPv6TestCase(AbstractTestCase, TestCase):
    """IP address Test"""

    def test_meta_single(self):
        request = HttpRequest()
        request.META = {'REMOTE_ADDR': self.REMOTE_ADDR}
        request.headers = {
            'X-FORWARDED-for': self.FORWARDED_HEADER,
        }
        with self.settings(IPWARE_REVERSE_PROXIES=[]):
            result = get_client_ip(request)
        self.assertEqual(result, ip_address(self.REMOTE_ADDR))

    def test_meta_multi_exact(self):
        request = HttpRequest()
        request.META = {
            'REMOTE_ADDR': self.REMOTE_ADDR,
        }
        request.headers = {
            'X-FORWARDED-for': self.FORWARDED_HEADER,
        }
        with self.settings(IPWARE_REVERSE_PROXIES=[
            ReverseProxy(Header("X-Forwarded-For"), self.REMOTE_ADDR, self.FORWARDED_ITEM_2, self.FORWARDED_ITEM_3)]):
            result = get_client_ip(request)
        self.assertEqual(result, ip_address(self.FORWARDED_ITEM_1))

    def test_meta_multi_from_proxy_itself(self):
        request = HttpRequest()
        request.META = {
            'REMOTE_ADDR': self.REMOTE_ADDR,
        }
        request.headers = {
            'X-FORWARDED-for': self.FORWARDED_HEADER,
        }
        with self.settings(IPWARE_REVERSE_PROXIES=[
            ReverseProxy(Header("X-Forwarded-For"), self.REMOTE_ADDR, self.FORWARDED_ITEM_1, self.FORWARDED_ITEM_2,
                         self.FORWARDED_ITEM_3)]):
            result = get_client_ip(request)
        self.assertEqual(result, ip_address(self.FORWARDED_ITEM_1))

    def test_meta_multi_with_unknown_headers(self):
        request = HttpRequest()
        request.META = {
            'REMOTE_ADDR': self.REMOTE_ADDR,
        }
        request.headers = {
            'X-FORWARDED-for': self.FORWARDED_HEADER,
        }
        with self.settings(IPWARE_REVERSE_PROXIES=[ReverseProxy(Header("X-Forwarded-For"), self.REMOTE_ADDR)]):
            result = get_client_ip(request)
        self.assertEqual(result, ip_address(self.FORWARDED_ITEM_3))

    def test_meta_proxy_order_left_most(self):
        request = HttpRequest()
        request.META = {
            'REMOTE_ADDR': self.REMOTE_ADDR,
        }
        request.headers = {
            'X-FORWARDED-for': self.FORWARDED_HEADER,
        }
        with self.settings(IPWARE_REVERSE_PROXIES=[
            ReverseProxy(Header("X-Forwarded-For", order=Order.HEADER_PREPENDED), self.REMOTE_ADDR)]):
            result = get_client_ip(request)
        self.assertEqual(result, ip_address(self.FORWARDED_ITEM_1))

    def test_meta_proxy_order_right_most(self):
        request = HttpRequest()
        request.META = {
            'REMOTE_ADDR': self.REMOTE_ADDR,
        }
        request.headers = {
            'X-FORWARDED-for': self.FORWARDED_HEADER,
        }
        with self.settings(IPWARE_REVERSE_PROXIES=[
            ReverseProxy(Header("X-Forwarded-For", order=Order.HEADER_APPENDED), self.REMOTE_ADDR)]):
            result = get_client_ip(request)
        self.assertEqual(result, ip_address(self.FORWARDED_ITEM_3))

    def test_meta_proxy_ignore_parsing_error(self):
        request = HttpRequest()
        request.META = {
            'REMOTE_ADDR': self.REMOTE_ADDR,
        }
        request.headers = {
            'X-FORWARDED-for': self.FORWARDED_HEADER_BOGUS,
        }
        with self.settings(IPWARE_REVERSE_PROXIES=[ReverseProxy(Header("X-Forwarded-For"), self.REMOTE_ADDR)]):
            result = get_client_ip(request)
        self.assertEqual(result, ip_address(self.FORWARDED_ITEM_3))

    def test_meta_proxy_parsing_error(self):
        request = HttpRequest()
        request.META = {
            'REMOTE_ADDR': self.REMOTE_ADDR,
        }
        request.headers = {
            'X-FORWARDED-for': self.FORWARDED_HEADER_UNKNOWN,
        }
        with self.settings(IPWARE_REVERSE_PROXIES=[ReverseProxy(Header("X-Forwarded-For"), self.REMOTE_ADDR)]):
            with self.assertRaises(Exception):
                result = get_client_ip(request)

    def tearDown(self) -> None:
        self.databases_handle.__exit__(None, None, None)

    def setUp(self) -> None:
        self.databases_handle = self.settings(DATABASES=[])
        self.databases_handle.__enter__()
        self.FORWARDED_HEADER_BOGUS = 'unknown,foo,::,bar,,,, 74dc::02ba, 74dc::02bb'
        self.FORWARDED_HEADER_UNKNOWN = '3ffe:1900:4545:3:200:f8ff:fe21:67cf, 74dc::02ba, unknown'
        self.REMOTE_ADDR = '74dc::02bc'
        self.FORWARDED_ITEM_1 = '3ffe:1900:4545:3:200:f8ff:fe21:67cf'
        self.FORWARDED_ITEM_2 = '74dc::02ba'
        self.FORWARDED_ITEM_3 = '74dc::02bb'
        self.FORWARDED_HEADER = '3ffe:1900:4545:3:200:f8ff:fe21:67cf, 74dc::02ba, 74dc::02bb'


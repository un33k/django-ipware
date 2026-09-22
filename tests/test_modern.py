"""The default (modern) algorithm: a thin adapter over python-ipware's modern engine."""

import ipaddress
import itertools
from typing import ClassVar

from django.http import HttpRequest
from django.test import SimpleTestCase, override_settings
from python_ipware import IpWare
from python_ipware.modern.parsers import TIER_GLOBAL, ip_tier

from ipware import get_client_ip

XFF = "HTTP_X_FORWARDED_FOR"


def request_with(meta):
    request = HttpRequest()
    request.META = meta
    return request


def resolve(meta, **kwargs):
    return get_client_ip(request_with(meta), **kwargs)


class DelegatesToModernEngine(SimpleTestCase):
    """Every option combination returns exactly what python-ipware's modern engine
    returns, as (str(ip), ip is globally routable)."""

    METAS: ClassVar = (
        {XFF: "177.139.233.139, 198.84.193.157, 198.84.193.158"},
        {XFF: "10.0.0.1, 177.139.233.139, 198.84.193.157"},
        {XFF: "unknown, 177.139.233.139, 198.84.193.157", "REMOTE_ADDR": "10.0.0.5"},
        {XFF: "224.0.0.1", "REMOTE_ADDR": "10.0.0.5"},
        {XFF: "[2606:4700::6810:84e5]:443, 198.84.193.157"},
        {"HTTP_FORWARDED": 'for="[2001:4860::17]:4711";proto=https'},
        {"HTTP_X_REAL_IP": "192.168.1.1", "REMOTE_ADDR": "127.0.0.1"},
        {"REMOTE_ADDR": "fec0::1"},
        {"REMOTE_ADDR": "64:ff9b::2d01:101"},
        {"REMOTE_ADDR": "8.8.8.8:abc"},
        {},
    )
    OPTIONS: ClassVar = {
        "proxy_order": ("left-most", "right-most"),
        "proxy_count": (None, 0, 1, 2),
        "proxy_trusted_ips": (None, ["198.84.193.157"], ["198.84."], ["198.84.0.0/16"]),
        "strict": (None, True, False),
    }

    def test_every_option_combination(self):
        checked = 0
        for meta in self.METAS:
            for values in itertools.product(*self.OPTIONS.values()):
                kw = dict(zip(self.OPTIONS, values, strict=True))
                engine = IpWare(
                    algorithm="modern",
                    leftmost=kw["proxy_order"] == "left-most",
                    proxy_count=kw["proxy_count"],
                    proxy_list=kw["proxy_trusted_ips"],
                )
                ip, _ = engine.get_client_ip(meta, kw["strict"] is not False)
                expected = (str(ip), ip_tier(ip) == TIER_GLOBAL) if ip else (None, False)
                with self.subTest(meta=meta, **kw):
                    self.assertEqual(resolve(meta, **kw), expected)
                checked += 1
        self.assertEqual(checked, len(self.METAS) * 2 * 4 * 4 * 3)


class BetterThanLegacy(SimpleTestCase):
    """Readable examples of where the default now differs from 7.x, each for the better."""

    def check_both(self, meta, modern, legacy, **kwargs):
        self.assertEqual(resolve(meta, **kwargs), modern)
        self.assertEqual(resolve(meta, algorithm="legacy", **kwargs), legacy)

    def test_public_hop_behind_private_first_hop(self):
        self.check_both({XFF: "10.0.0.1, 177.139.233.139"}, ("177.139.233.139", True), ("10.0.0.1", False))

    def test_multicast_is_never_the_client(self):
        meta = {XFF: "224.0.0.1", "REMOTE_ADDR": "10.0.0.5"}
        self.check_both(meta, ("10.0.0.5", False), ("224.0.0.1", True))

    def test_site_local_is_not_routable(self):
        self.check_both({"REMOTE_ADDR": "fec0::1"}, ("fec0::1", False), ("fec0::1", True))

    def test_rfc7239_forwarded(self):
        meta = {"HTTP_FORWARDED": 'for="[2001:4860::17]:4711";proto=https'}
        self.check_both(meta, ("2001:4860::17", True), (None, False))

    def test_trusted_proxy_entry_is_exact(self):
        meta = {XFF: "177.139.233.139, 198.84.193.157"}
        self.check_both(meta, (None, False), ("177.139.233.139", True), proxy_trusted_ips=["198.84.193.15"])

    def test_malformed_port_rejected(self):
        self.check_both({"REMOTE_ADDR": "8.8.8.8:abc"}, (None, False), ("8.8.8.8", True))


class SettingsAndArguments(SimpleTestCase):
    """Settings apply only when the matching argument is not given."""

    META: ClassVar = {XFF: "177.139.233.139", "REMOTE_ADDR": "8.8.8.8"}

    def test_no_settings_uses_python_ipware_defaults(self):
        self.assertEqual(resolve(self.META), ("177.139.233.139", True))

    @override_settings(IPWARE_META_PRECEDENCE_ORDER=("REMOTE_ADDR",))
    def test_header_order_setting_applies(self):
        self.assertEqual(resolve(self.META), ("8.8.8.8", True))

    @override_settings(IPWARE_META_PRECEDENCE_ORDER=("REMOTE_ADDR",))
    def test_header_order_argument_beats_setting(self):
        self.assertEqual(resolve(self.META, request_header_order=[XFF]), ("177.139.233.139", True))

    @override_settings(IPWARE_META_PRECEDENCE_ORDER=())
    def test_empty_header_order_setting_means_defaults(self):
        self.assertEqual(resolve(self.META), ("177.139.233.139", True))

    @override_settings(IPWARE_STRICT=False)
    def test_strict_setting_applies(self):
        self.assertEqual(resolve({XFF: "unknown, 177.139.233.139"}), ("177.139.233.139", True))

    @override_settings(IPWARE_STRICT=False)
    def test_strict_argument_beats_setting(self):
        self.assertEqual(resolve({XFF: "unknown, 177.139.233.139"}, strict=True), (None, False))

    def test_strict_by_default(self):
        self.assertEqual(resolve({XFF: "unknown, 177.139.233.139"}), (None, False))

    @override_settings(IPWARE_META_PROXY_COUNT=1)
    def test_proxy_count_setting_applies(self):
        # Restored from 6.x (#127): a single-hop chain no longer satisfies one proxy.
        self.assertEqual(resolve({XFF: "177.139.233.139"}), (None, False))
        self.assertEqual(resolve({XFF: "177.139.233.139, 198.84.193.157"}), ("177.139.233.139", True))

    @override_settings(IPWARE_META_PROXY_COUNT=1)
    def test_proxy_count_argument_beats_setting(self):
        self.assertEqual(resolve({XFF: "177.139.233.139"}, proxy_count=0), ("177.139.233.139", True))


class InputsAndValidation(SimpleTestCase):
    META: ClassVar = {XFF: "177.139.233.139, 198.84.193.157"}

    def test_right_most(self):
        self.assertEqual(resolve(self.META, proxy_order="right-most"), ("198.84.193.157", True))

    def test_one_shot_iterables_are_accepted(self):
        result = resolve(
            self.META,
            proxy_trusted_ips=(ip for ip in ["198.84.193.157"]),
            request_header_order=(h for h in [XFF]),
        )
        self.assertEqual(result, ("177.139.233.139", True))

    def test_private_client_is_not_routable(self):
        self.assertEqual(resolve({XFF: "10.0.0.1"}), ("10.0.0.1", False))

    def test_nothing_found(self):
        self.assertEqual(resolve({}), (None, False))

    def test_ipv4_mapped_is_returned_as_ipv4(self):
        ip, routable = resolve({"REMOTE_ADDR": "::ffff:177.139.233.139"})
        self.assertEqual((ip, routable), ("177.139.233.139", True))
        self.assertIsInstance(ipaddress.ip_address(ip), ipaddress.IPv4Address)

    def test_misconfiguration_raises(self):
        cases = [
            {"proxy_order": "bogus"},
            {"proxy_trusted_ips": "198.84.193.157"},  # bare string, not a list
            {"proxy_trusted_ips": ["", "10."]},
            {"proxy_trusted_ips": ["not-an-ip"]},
            {"proxy_count": -1},
            {"request_header_order": "REMOTE_ADDR"},
        ]
        for kwargs in cases:
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                resolve(self.META, **kwargs)

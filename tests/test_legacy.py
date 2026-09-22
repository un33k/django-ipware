"""The frozen 7.x behavior, selected with algorithm="legacy".

tests/legacy/tests_ip.py is the untouched 7.x suite; discovery runs it on the
default (modern) algorithm, and V7SuiteOnLegacy re-runs it on legacy.
"""

import ipaddress
import itertools
from typing import ClassVar

from django.http import HttpRequest
from django.test import SimpleTestCase, override_settings
from python_ipware import LegacyIpWare

from ipware import get_client_ip
from tests.legacy import tests_ip as v7


def request_with(meta):
    request = HttpRequest()
    request.META = meta
    return request


@override_settings(IPWARE_ALGORITHM="legacy")
class V7SuiteOnLegacy(v7.IpTestCase):
    """The original 7.x tests, run against the frozen legacy function."""


class LegacyMatchesV3Engine(SimpleTestCase):
    """Legacy must be exactly python-ipware's frozen v3 engine, strict by default."""

    METAS: ClassVar = (
        {"HTTP_X_FORWARDED_FOR": "177.139.233.139, 198.84.193.157, 198.84.193.158"},
        {"HTTP_X_FORWARDED_FOR": "10.0.0.1, 177.139.233.139"},  # v3 returns the private first hop
        {"HTTP_X_FORWARDED_FOR": "unknown, 177.139.233.139", "REMOTE_ADDR": "10.0.0.5"},
        {"HTTP_X_FORWARDED_FOR": "224.0.0.1"},  # v3 returns multicast as routable
        {"REMOTE_ADDR": "fec0::1"},
        {"REMOTE_ADDR": "8.8.8.8:abc"},  # v3 truncates a malformed port
        {"HTTP_X_REAL_IP": "192.168.1.1", "REMOTE_ADDR": "127.0.0.1"},
        {},
    )
    OPTIONS: ClassVar = {
        "proxy_order": ("left-most", "right-most"),
        "proxy_count": (None, 0, 1, 2),
        "proxy_trusted_ips": (None, ["198.84.193.158"], ["198.84."]),
        "strict": (True, False),
    }

    def test_every_option_combination(self):
        checked = 0
        for meta in self.METAS:
            for values in itertools.product(*self.OPTIONS.values()):
                kw = dict(zip(self.OPTIONS, values, strict=True))
                engine = LegacyIpWare(
                    leftmost=kw["proxy_order"] == "left-most",
                    proxy_count=kw["proxy_count"],
                    proxy_list=kw["proxy_trusted_ips"],
                )
                ip, _ = engine.get_client_ip(meta, kw["strict"])
                expected = (str(ip), ip.is_global) if ip else (None, False)
                with self.subTest(meta=meta, **kw):
                    self.assertEqual(get_client_ip(request_with(meta), algorithm="legacy", **kw), expected)
                checked += 1
        self.assertEqual(checked, len(self.METAS) * 2 * 4 * 3 * 2)

    def test_default_is_strict(self):
        meta = {"HTTP_X_FORWARDED_FOR": "unknown, 177.139.233.139"}
        self.assertEqual(get_client_ip(request_with(meta), algorithm="legacy"), (None, False))


class LegacyQuirksArePreserved(SimpleTestCase):
    """7.x behaviors that modern fixes, pinned so legacy never drifts."""

    META: ClassVar = {"HTTP_X_FORWARDED_FOR": "177.139.233.139", "REMOTE_ADDR": "8.8.8.8"}

    @override_settings(IPWARE_META_PRECEDENCE_ORDER=("REMOTE_ADDR",))
    def test_setting_overrides_explicit_header_order(self):
        result = get_client_ip(
            request_with(self.META), request_header_order=["HTTP_X_FORWARDED_FOR"], algorithm="legacy"
        )
        self.assertEqual(result, ("8.8.8.8", True))

    @override_settings(IPWARE_STRICT=True)
    def test_setting_overrides_explicit_strict(self):
        meta = {"HTTP_X_FORWARDED_FOR": "unknown, 177.139.233.139"}
        self.assertEqual(get_client_ip(request_with(meta), strict=False, algorithm="legacy"), (None, False))

    @override_settings(IPWARE_META_PROXY_COUNT=5)
    def test_proxy_count_setting_is_ignored(self):
        meta = {"HTTP_X_FORWARDED_FOR": "177.139.233.139"}
        self.assertEqual(get_client_ip(request_with(meta), algorithm="legacy"), ("177.139.233.139", True))

    def test_unknown_proxy_order_means_right_most(self):
        meta = {"HTTP_X_FORWARDED_FOR": "177.139.233.139, 198.84.193.157"}
        self.assertEqual(
            get_client_ip(request_with(meta), proxy_order="bogus", algorithm="legacy"), ("198.84.193.157", True)
        )

    def test_routable_is_python_is_global(self):
        self.assertEqual(ipaddress.ip_address("fec0::1").is_global, True)
        self.assertEqual(get_client_ip(request_with({"REMOTE_ADDR": "fec0::1"}), algorithm="legacy"), ("fec0::1", True))

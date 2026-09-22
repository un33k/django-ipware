"""Algorithm selection: the argument wins, then IPWARE_ALGORITHM, then "auto" (modern)."""

from django.apps import apps
from django.http import HttpRequest
from django.test import SimpleTestCase, override_settings

import ipware
from ipware import get_client_ip

# Legacy returns the private first hop; modern finds the public one.
META = {"HTTP_X_FORWARDED_FOR": "10.0.0.1, 177.139.233.139"}
MODERN = ("177.139.233.139", True)
LEGACY = ("10.0.0.1", False)


def resolve(**kwargs):
    request = HttpRequest()
    request.META = META
    return get_client_ip(request, **kwargs)


class AlgorithmSelection(SimpleTestCase):
    def test_default_is_modern(self):
        self.assertEqual(resolve(), MODERN)

    def test_explicit_algorithms(self):
        self.assertEqual(resolve(algorithm="auto"), MODERN)
        self.assertEqual(resolve(algorithm="modern"), MODERN)
        self.assertEqual(resolve(algorithm="legacy"), LEGACY)

    @override_settings(IPWARE_ALGORITHM="legacy")
    def test_setting_selects_legacy(self):
        self.assertEqual(resolve(), LEGACY)

    @override_settings(IPWARE_ALGORITHM="legacy")
    def test_argument_beats_setting(self):
        self.assertEqual(resolve(algorithm="modern"), MODERN)

    def test_unknown_algorithm_raises(self):
        with self.assertRaises(ValueError):
            resolve(algorithm="bogus")

    @override_settings(IPWARE_ALGORITHM="bogus")
    def test_unknown_algorithm_setting_raises(self):
        with self.assertRaises(ValueError):
            resolve()


class PublicSurface(SimpleTestCase):
    def test_exports(self):
        self.assertEqual(sorted(ipware.__all__), ["__version__", "get_client_ip"])
        self.assertEqual(ipware.__version__, "8.0.0")

    def test_app_config(self):
        self.assertEqual(apps.get_app_config("ipware").name, "ipware")

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from . import defaults

class IPwareConfig(AppConfig):
    """
    Configuration entry point for the ipware app
    """
    label = name = 'ipware'
    verbose_name = _("ipware app")

    def ready(self):
        # Copy all default attrs into the user's settings module if
        # they're not defined there.
        for attr in ('IPWARE_META_PRECEDENCE_ORDER', 'IPWARE_PRIVATE_IP_PREFIX', 'IPWARE_LOOPBACK_PREFIX'):
            default_value = getattr(defaults, attr)
            setattr(settings, attr, getattr(settings, attr, default_value))

        # A bit hacky, ensure we always append standard prefixes
        settings.IPWARE_PRIVATE_IP_PREFIX = tuple(settings.IPWARE_PRIVATE_IP_PREFIX) + (
            '::',  # Unspecified address
            '::ffff:', '2001:10:', '2001:20:'  # messages to software
            '2001::',  # TEREDO
            '2001:2::',  # benchmarking
            '2001:db8:',  # reserved for documentation and example code
            'fc00:',  # IPv6 private block
            'fe80:',  # link-local unicast
            'ff00:',  # IPv6 multicast
        )

from warnings import warn

from django.conf import settings


# Search for the real IP address in the following order
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Forwarded-For
# X-Forwarded-For: <client>, <proxy1>, <proxy2>
# Configurable via settings.py

def IPWARE_REVERSE_PROXIES():
    return getattr(settings,
        'IPWARE_REVERSE_PROXIES', []
    )
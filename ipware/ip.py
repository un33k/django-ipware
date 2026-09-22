"""Django-facing API: ``get_client_ip(request)``.

A thin adapter over python-ipware. The resolution algorithm, header parsing
and trusted-proxy matching all live in python-ipware; this module maps Django
settings and arguments onto it.

Algorithms
----------
* ``"modern"`` (the default): python-ipware's modern engine. Upgrading users
  pass nothing. An explicit argument always wins over the matching Django setting.
* ``"legacy"``: the frozen django-ipware 7.x function, byte-for-byte
  behavior, including its quirk that settings override explicit arguments.

Django settings (all optional)
------------------------------
``IPWARE_ALGORITHM``             ``"modern"`` (default) | ``"legacy"``
``IPWARE_META_PRECEDENCE_ORDER`` header keys to check, in order
``IPWARE_META_PROXY_COUNT``      expected number of proxies
``IPWARE_STRICT``                strict chain validation (default ``True``)
"""

from collections.abc import Iterable
from typing import Literal, Optional, Tuple

from django.conf import settings
from django.http import HttpRequest
from python_ipware import IpWare
from python_ipware.modern.parsers import TIER_GLOBAL, ip_tier

from . import legacy

Algorithm = Literal["modern", "legacy"]
ProxyOrder = Literal["left-most", "right-most"]

_ALGORITHMS = ("modern", "legacy")
_PROXY_ORDERS = ("left-most", "right-most")


def _setting(name: str, value):
    """An explicit (non-None) argument wins; otherwise the Django setting, if set."""
    return value if value is not None else getattr(settings, name, None)


def _materialize(values):
    """Turn a one-shot iterable into a list so python-ipware can validate and use it.

    A bare string is passed through unchanged so python-ipware rejects it instead
    of splitting it into one entry per character.
    """
    if values is None or isinstance(values, str):
        return values
    return list(values)


def get_client_ip(
    request: HttpRequest,
    proxy_order: ProxyOrder = "left-most",
    proxy_count: Optional[int] = None,
    proxy_trusted_ips: Optional[Iterable[str]] = None,
    request_header_order: Optional[Iterable[str]] = None,
    strict: Optional[bool] = None,
    *,
    algorithm: Optional[Algorithm] = None,
) -> Tuple[Optional[str], bool]:
    """Return ``(client_ip, is_routable)``.

    ``client_ip`` is the best client IP as a string, or ``None`` when none was
    found. ``is_routable`` is True when that address is publicly routable.

    Raises ``ValueError`` on misconfiguration: an unknown ``algorithm`` or
    ``proxy_order``, or an invalid proxy list, header order or proxy count.
    """
    algorithm = _setting("IPWARE_ALGORITHM", algorithm) or "modern"
    if algorithm not in _ALGORITHMS:
        msg = f"algorithm must be one of {_ALGORITHMS}, got {algorithm!r}"
        raise ValueError(msg)

    if algorithm == "legacy":
        return legacy.get_client_ip(
            request,
            proxy_order=proxy_order,
            proxy_count=proxy_count,
            proxy_trusted_ips=proxy_trusted_ips,
            request_header_order=request_header_order,
            strict=True if strict is None else strict,
        )

    if proxy_order not in _PROXY_ORDERS:
        msg = f"proxy_order must be one of {_PROXY_ORDERS}, got {proxy_order!r}"
        raise ValueError(msg)

    strict = _setting("IPWARE_STRICT", strict)
    ipw = IpWare(
        precedence=_materialize(_setting("IPWARE_META_PRECEDENCE_ORDER", request_header_order)),
        leftmost=proxy_order == "left-most",
        proxy_count=_setting("IPWARE_META_PROXY_COUNT", proxy_count),
        proxy_list=_materialize(proxy_trusted_ips),
        algorithm="modern",
    )
    ip, _trusted = ipw.get_client_ip(request.META, True if strict is None else bool(strict))
    if ip is None:
        return None, False
    return str(ip), ip_tier(ip) == TIER_GLOBAL

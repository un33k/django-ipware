"""Frozen django-ipware 7.x behavior.

``ip.py`` is the 7.x ``get_client_ip`` (including the non-strict option from
#122), changed in one line only: it imports python-ipware's frozen v3 engine
(``LegacyIpWare``) so results stay exactly as in 7.x on python-ipware 4.x.
This package takes no further changes; select it with ``algorithm="legacy"``
or ``IPWARE_ALGORITHM = "legacy"``.
"""

from .ip import get_client_ip

__all__ = ["get_client_ip"]

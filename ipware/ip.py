from typing import Iterable, Literal, Optional, Tuple

from django.conf import settings
from django.http import HttpRequest
from python_ipware import IpWare


def get_client_ip(
    request: HttpRequest,
    proxy_order: Literal['left-most', 'right-most'] = 'left-most',
    proxy_count: Optional[int] = None,
    proxy_trusted_ips: Optional[Iterable[str]] = None,
    request_header_order: Optional[Iterable[str]] = None,
) -> Tuple[str, bool]:
    leftmost = proxy_order == 'left-most'
    request_header_order = getattr(settings, 'IPWARE_META_PRECEDENCE_ORDER', request_header_order)

    # Instantiate IpWare with values from the function arguments
    ipw = IpWare(precedence=request_header_order,
                 leftmost=leftmost,
                 proxy_count=proxy_count,
                 proxy_list=proxy_trusted_ips)

    ip, _ = ipw.get_client_ip(request.META, True)

    client_ip = None
    routable = False

    if ip:
        client_ip = str(ip)
        routable = ip.is_global

    return client_ip, routable

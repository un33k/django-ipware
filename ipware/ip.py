from django.conf import settings
from python_ipware import IpWare


def get_client_ip(
    request,
    proxy_order='left-most',
    proxy_count=None,
    proxy_trusted_ips=None,
    request_header_order=None,
):
    leftmost = proxy_order == 'left-most'
    proxy_count = proxy_count if proxy_count is not None else getattr(settings, 'IPWARE_META_PROXY_COUNT', 0)
    proxy_list = proxy_trusted_ips if proxy_trusted_ips is not None else []
    request_header_order = getattr(settings, 'IPWARE_META_PRECEDENCE_ORDER', request_header_order)

    # Instantiate IpWare with values from the function arguments
    ipw = IpWare(precedence=request_header_order,
                 leftmost=leftmost,
                 proxy_count=proxy_count,
                 proxy_list=proxy_list)

    ip, _ = ipw.get_client_ip(request.META, True)

    client_ip = None
    routable = False

    if ip:
        client_ip = str(ip)
        routable = ip.is_global

    return client_ip, routable

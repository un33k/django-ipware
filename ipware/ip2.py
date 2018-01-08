from . import utils as util
from . import defaults as defs


def get_client_ip(
    request,
    proxy_order='left-most',
    proxy_count=defs.IPWARE_PROXY_COUNT,
    proxy_trusted_ips=defs.IPWARE_TRUSTED_PROXY_LIST
):
    client_ip = None
    routable = False

    for key in defs.IPWARE_META_PRECEDENCE_ORDER:
        value = util.get_request_meta(request, key)
        if value:
            ips, ip_count = util.get_ip_info_from_string(value)

            if proxy_count > 0 and proxy_count != ip_count - 1:
                # not meeting the fixed number of specified proxies
                continue

            if ip_count > 1:
                if proxy_order == 'right-most':
                    # handle custom proxy configuration
                    # X-Forwarded-For: <proxy2>, <proxy1>, <client>
                    ips.reverse()

                for proxy in proxy_trusted_ips:
                    if proxy in ips[-1]:
                        client_ip, routable = util.validate_ip(ips[0])
                        if client_ip and routable:
                            return client_ip, routable

            client_ip, routable = util.validate_ip(ips[0])
            if client_ip and routable:
                return client_ip, routable

    return client_ip, routable

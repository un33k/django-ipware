from . import utils as util
from . import defaults as defs


def get_ip(request, real_ip_only=False, right_most_proxy=False):
    """
    Returns client's best-matched ip-address, or None
    """
    best_matched_ip = None
    for key in defs.IPWARE_META_PRECEDENCE_ORDER:
        value = util.get_request_meta(request, key)
        if value is not None:
            ips, ip_count = util.get_ip_info_from_string(value)
            if right_most_proxy and ip_count > 1:
                ips = reversed(ips)
            for ip_str in ips:
                if ip_str and util.is_valid_ip(ip_str):
                    if util.is_public_ip(ip_str):
                        return ip_str
                    if not real_ip_only:
                        if best_matched_ip is None:
                            best_matched_ip = ip_str
                        elif util.is_loopback(best_matched_ip) and not util.is_loopback(ip_str):
                            best_matched_ip = ip_str
    return best_matched_ip


def get_real_ip(request, right_most_proxy=False):
    """
    Returns client's best-matched `real` `externally-routable` ip-address, or None
    """
    return get_ip(request, real_ip_only=True, right_most_proxy=right_most_proxy)


def get_trusted_ip(request, right_most_proxy=False, trusted_proxies=defs.IPWARE_TRUSTED_PROXY_LIST):
    """
    Returns client's ip-address from `trusted` proxy server(s) or None
    """
    if trusted_proxies:
        meta_keys = ['HTTP_X_FORWARDED_FOR', 'X_FORWARDED_FOR']
        for key in meta_keys:
            value = request.META.get(key, request.META.get(key.replace('_', '-'), '')).strip()
            if value:
                ips, ip_count = util.get_ip_info_from_string(value)
                if ip_count > 1:
                    if right_most_proxy:
                        ips.reverse()
                    for proxy in trusted_proxies:
                        if proxy in ips[-1]:
                            return ips[0]
    return None

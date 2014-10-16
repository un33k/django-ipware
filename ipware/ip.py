
from .utils import is_valid_ip
from .defaults import IPWARE_META_PRECEDENCE_ORDER
from .defaults import IPWARE_NON_PUBLIC_IP_PREFIX


def get_ip(request, real_ip_only=False):
    """
    Returns client's best-matched ip-address, or None
    """
    best_matched_ip = None
    for key in IPWARE_META_PRECEDENCE_ORDER:
        value = request.META.get(key, '').strip()
        if value != '':
            ips = [ip.strip().lower() for ip in value.split(',')]
            for ip_str in ips:
                if ip_str and is_valid_ip(ip_str):
                    if not ip_str.startswith(IPWARE_NON_PUBLIC_IP_PREFIX):
                        return ip_str
                    elif not real_ip_only:
                        loopback = ('127.0.0.1', '::1')
                        if best_matched_ip is None:
                            best_matched_ip = ip_str
                        elif best_matched_ip in loopback and ip_str not in loopback:
                            best_matched_ip = ip_str
    return best_matched_ip


def get_real_ip(request):
    """
    Returns client's best-matched `real` ip-address, or None
    """
    return get_ip(request, real_ip_only=True)

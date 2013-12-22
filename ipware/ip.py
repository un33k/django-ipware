
from utils import is_valid_ip
from defaults import IPWARE_META_PRECEDENCE_LIST
from defaults import IPWARE_PRIVATE_IP_PREFIX


def get_real_ip(request):
    """
    Best attempt to get client's real ip-address or returns None
    """
    for key in IPWARE_META_PRECEDENCE_LIST:
        value = request.META.get(key, '')
        if value.strip() != '':
            ips = [ip.strip() for ip in value.split(',')]
            for ip_str in ips:
                if ip_str and not ip_str.startswith(IPWARE_PRIVATE_IP_PREFIX):
                    if is_valid_ip(ip_str):
                        return ip_str
    return None

def get_ip_address_from_request(request):
    """
    Backwards compatibility -- use get_real_ip() instead
    """
    return get_real_ip(request)


import socket

from . import defaults as defs


NON_PUBLIC_IP_PREFIX = tuple([ip.lower() for ip in defs.IPWARE_NON_PUBLIC_IP_PREFIX])
TRUSTED_PROXY_LIST = tuple([ip.lower() for ip in defs.IPWARE_TRUSTED_PROXY_LIST])


def is_valid_ipv4(ip_str):
    """
    Check the validity of an IPv4 address
    """
    try:
        socket.inet_pton(socket.AF_INET, ip_str)
    except AttributeError:  # pragma: no cover
        try:  # Fall-back on legacy API or False
            socket.inet_aton(ip_str)
        except (AttributeError, socket.error):
            return False
        return ip_str.count('.') == 3
    except socket.error:
        return False
    return True


def is_valid_ipv6(ip_str):
    """
    Check the validity of an IPv6 address
    """
    try:
        socket.inet_pton(socket.AF_INET6, ip_str)
    except socket.error:
        return False
    return True


def is_valid_ip(ip_str):
    """
    Check the validity of an IP address
    """
    return is_valid_ipv4(ip_str) or is_valid_ipv6(ip_str)


def is_private_ip(ip_str):
    """
    Returns true of ip_str is private & not routable, else return false
    """
    ip = ip_str.strip().lower()
    return ip.startswith(NON_PUBLIC_IP_PREFIX)


def is_public_ip(ip_str):
    """
    Returns true of ip_str is public & routable, else return false
    """
    ip = ip_str.strip().lower()
    return not ip.startswith(NON_PUBLIC_IP_PREFIX)


def is_loopback(ip_str):
    """
    Returns true of ip_str is public & routable, else return false
    """
    ip = ip_str.strip()
    return ip in defs.IPWARE_LOOPBACK_PREFIX


def get_request_meta(request, key):
    """
    Given a key, it returns a cleaned up version of the value from request.META, or None
    """
    value = request.META.get(key, request.META.get(key.replace('_', '-'), '')).strip()
    if value == '':
        return None
    return value


def get_ip_info_from_string(ip_str):
    """
    Given a string, it returns one or more `,` separated IP addresses
    """
    ip_list = [ip.strip().lower() for ip in ip_str.split(',')]
    return ip_list, len(ip_list)


def validate_ip(ip_str):
    """
    Validates IP address and returns IP & whether IP is routable
    """
    ip = None
    is_routable_ip = False
    if is_valid_ip(ip_str):
        ip = ip_str
        is_routable_ip = is_public_ip(ip)
    return ip, is_routable_ip

import email.utils
import socket

from . import defaults as defs


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
    return ip_str.startswith(defs.IPWARE_NON_PUBLIC_IP_PREFIX)


def is_public_ip(ip_str):
    """
    Returns true of ip_str is public & routable, else return false
    """
    return not is_private_ip(ip_str)


def is_loopback_ip(ip_str):
    """
    Returns true of ip_str is public & routable, else return false
    """
    return ip_str.startswith(defs.IPWARE_LOOPBACK_PREFIX)


def get_request_meta(request, key):
    """
    Given a key, it returns a cleaned up version of the value from request.META, or None
    """
    value = request.META.get(key, request.META.get(key.replace('_', '-'), '')).strip()
    if value == '':
        return None
    return value


def get_ips_from_string(ip_str):
    """
    Given a string, it returns a list of one or more valid IP addresses
    """
    ip_list = []

    for ip in ip_str.split(','):
        clean_ip = ip.strip().lower()
        if clean_ip:
            ip_list.append(clean_ip)

    ip_count = len(ip_list)
    if ip_count > 0:
        if is_valid_ip(ip_list[0]) and is_valid_ip(ip_list[-1]):
            return ip_list, ip_count

    return [], 0


def _parse_node_identifier(node):
    """
    Parse RFC 7239's node.

    https://tools.ietf.org/html/rfc7239#section-6
    """
    values = {}
    elements = node.rsplit(':', 1)
    if len(elements) == 2 and ']' in elements[1]:
        elements = [node]  # don't split inside IPv6
    values['name'] = elements[0]
    if len(elements) == 2:
        if elements[1].startswith('_'):  # obfport
            values['port'] = elements[1]
        else:
            values['port'] = int(elements[1])
    return values


def _parse_forwarded_pair(forwarded_pair):
    """
    Parse RFC 7239's forwarded-pair.

    https://tools.ietf.org/html/rfc7239#section-4
    """
    key, value = ''.join(forwarded_pair).split('=', 1)
    key = key.lower()
    value = email.utils.unquote(value)
    if key == 'for':
        return key, _parse_node_identifier(node=value)
    else:
        return key, value


def _parse_http_list(list, delimiter=','):
    """
    Split a list where the entries may contain quoted strings.

    The list extention [1] and quoted-string [2] are defined in RFC
    7230.  The delimiter defaults to ',', which matches [1].

    You can override the delimiter to parse structures like RFC 7239's
    forwarded-element into forwarded-pairs [3], in which case you
    would set delimiter=';'.

    [1]: https://tools.ietf.org/html/rfc7230#section-7
    [2]: https://tools.ietf.org/html/rfc7230#section-3.2.6
    [3]: https://tools.ietf.org/html/rfc7239#section-4
    """
    entry = []
    in_escape = in_quote = False
    for char in list:
        if char == '\\' and in_quote:
            in_escape = not in_escape
        elif in_escape:
            in_escape = False
        elif char == '"':
            in_quote = not in_quote
        if char == delimiter and not in_quote:
            yield ''.join(entry).strip()
            entry = []
        else:
            entry.append(char)
    if entry:
        yield ''.join(entry).strip()


def get_ips_from_forwarded_string(ip_str):
    """
    Given a string, it returns a list of one or more valid IP addresses
    """
    ip_list = []

    for forwarded_element in _parse_http_list(ip_str, delimiter=','):
        for pair in _parse_http_list(forwarded_element, delimiter=';'):
            key, value = _parse_forwarded_pair(forwarded_pair=''.join(pair))
            if key == 'for':
                name = value['name']
                if name.startswith('['):  # IPv6
                    name = name.lstrip('[').rstrip(']')
                ip_list.append(name)

    ip_count = len(ip_list)
    if ip_count == 0:
        raise ValueError('at least one forwarded-element is required')
    return ip_list, ip_count


def get_ip_info(ip_str):
    """
    Given a string, it returns a tuple of (IP, Routable).
    """
    ip = None
    is_routable_ip = False
    if is_valid_ip(ip_str):
        ip = ip_str
        is_routable_ip = is_public_ip(ip)
    return ip, is_routable_ip


def get_best_ip(last_ip, next_ip):
    """
    Given two IP addresses, it returns the the best match ip.
    Order of precedence is (Public, Private, Loopback, None)
    Right-most IP is returned
    """
    if last_ip is None:
        return next_ip
    if is_public_ip(last_ip) and not is_public_ip(next_ip):
        return last_ip
    if is_private_ip(last_ip) and is_loopback_ip(next_ip):
        return last_ip
    return next_ip

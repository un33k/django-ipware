
from .utils import is_valid_ip
from .defaults import IPWARE_META_IP_ADDRESS_HEADER
from .defaults import IPWARE_META_PRECEDENCE_ORDER
from .defaults import IPWARE_NON_PUBLIC_IP_PREFIX

import warnings


def _get_ip_from_header_value(value, real_ip_only=False, best_matched_ip=None, right_most_proxy=False):
    """
    Scans `value` and returns a two-tuple with an IP and a boolean to express whether or not the IP is real.

    `value` should be the header value from an HTTP header such as `X-Forwarded-For`.

    The returned tuple takes the form: ({IP_ADDRESS}, {IS_REAL}).

    The returned IP may be `None` if no good candidate IPs are found in `value`.

    If `real_ip_only` is `False`, good candidate IPs include any well-formed IP, including
    internal and loopback IPs. Otherwise, good candidate IPs must be well-formed external IPs.

    :param value: HTTP header value that contains a chain of IP addresses
    :param real_ip_only: when `True`, this function only returns well-formed external IPs
    :param best_matched_ip: an already-discovered IP for the request in question. Returned
                            in the two-tuple unless a better match is found
    :param right_most_proxy: whether or not to iterate over IPs in reverse order
    :return: a two-tuple with the IP address and a boolean to express whether or not the IP is real
    """
    assert value != '', "Empty value passed to function."

    ips = [ip.strip().lower() for ip in value.split(',')]
    if right_most_proxy:
        ips = reversed(ips)
    for ip_str in ips:
        if ip_str and is_valid_ip(ip_str):
            if not ip_str.startswith(IPWARE_NON_PUBLIC_IP_PREFIX):
                return ip_str, True
            elif not real_ip_only:
                loopback = ('127.0.0.1', '::1')
                if best_matched_ip is None:
                    best_matched_ip = ip_str
                elif best_matched_ip in loopback and ip_str not in loopback:
                    best_matched_ip = ip_str

    return best_matched_ip, False


def _get_ip_using_ip_address_header(request, real_ip_only=False, right_most_proxy=False):
    """ Returns best matched IP address based on the `IPWARE_META_IP_ADDRESS_HEADER` setting.

    :param request: the current HTTP request
    :param real_ip_only: when `True`, this function only returns well-formed external IPs
    :param right_most_proxy: whether or not to iterate over IPs in reverse order
    :return: the best matched client IP address for `request`, or `None` if no match is found
    """
    value = request.META.get(IPWARE_META_IP_ADDRESS_HEADER, '').strip()
    if value != '':
        return _get_ip_from_header_value(value, real_ip_only=real_ip_only, right_most_proxy=right_most_proxy)[0]
    else:
        return None


def _get_ip_using_precedence_order(request, real_ip_only=False, right_most_proxy=False):
    """ Returns best matched IP address based on the `IPWARE_META_PRECEDENCE_ORDER` setting.

    Iterates over each header in order. Whenever a real (well-formed, external) IP address
    is found in a particular header, it's returned right away. Otherwise, if an internal or
    loopback IP is found, it's stored and returned if `real_ip_only` is `True` and there are
    no subsequent external IPs.

    :param request: the current HTTP request
    :param real_ip_only: when `True`, this function only returns well-formed external IPs
    :param right_most_proxy: whether or not to iterate over IPs in reverse order
    :return: the best matched IP client address for `request`, or `None` if no match is found
    """
    best_matched_ip = None
    for key in IPWARE_META_PRECEDENCE_ORDER:
        value = request.META.get(key, '').strip()
        if value != '':
            header_ip, is_real_ip = _get_ip_from_header_value(value, real_ip_only, best_matched_ip, right_most_proxy)
            if is_real_ip:
                return header_ip
            else:
                best_matched_ip = header_ip

    return best_matched_ip


def get_ip(request, real_ip_only=False, right_most_proxy=False):
    """ Returns client's best-matched ip-address, or `None` """
    if not IPWARE_META_IP_ADDRESS_HEADER:
        warnings.warn("The use of header precedence ordering is deprecated. "
                      "To avoid this warning, set IPWARE_META_IP_ADDRESS_HEADER "
                      "to a header forwarded by trusted proxies.",
                      DeprecationWarning)
        return _get_ip_using_precedence_order(request, real_ip_only, right_most_proxy=right_most_proxy)
    else:
        return _get_ip_using_ip_address_header(request, real_ip_only, right_most_proxy=right_most_proxy)


def get_real_ip(request, right_most_proxy=False):
    """ Returns client's best-matched real (well-formed, external) ip-address, or `None` """
    return get_ip(request, real_ip_only=True, right_most_proxy=right_most_proxy)

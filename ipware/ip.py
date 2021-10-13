from ipaddress import IPv4Address, IPv6Address, ip_address
from typing import Union

from . import defaults as defs
from warnings import warn

from .descriptor import ReverseProxy, Order

REMOTE_ADDR = 'REMOTE_ADDR'

import logging
log = logging.getLogger(__name__)

def get_client_ip(
        request: 'django.http.request.HttpRequest',
):
    """
    This will return the outmost provable IP address.
    This also means, if you misconfigured your reverse proxy or this library:
    * This might always return your reverse proxy's IP (and the non-global flag), if a reverse proxy is not configured
    * This might (almost) always return your reverse proxy's IP (and the non-global flag), if an expected header is missing.
    * This might return a forged IP (and the non-global flag), if an expected header missing is set by someone else.
    """
    request_remote_addr = ip_address(request.META[REMOTE_ADDR])
    # this ip address is trusted to be correct under the assumption that spoofing or MITM is prevented by other measures.
    outmost_proven_ip: Union[IPv4Address, IPv6Address] = request_remote_addr

    headers = {field_name.upper(): field_value for field_name, field_value in request.headers.items()}

    while True:
        proxies = defs.IPWARE_REVERSE_PROXIES()
        matching_reverse_proxy_definitions = _get_matching_proxy_definitions(outmost_proven_ip, proxies)

        if len(matching_reverse_proxy_definitions) > 1:
            raise Exception(
                "Unable to correctly determine client IP due to duplicate proxy IP addresses (or non-disjunct networks)")

        if len(matching_reverse_proxy_definitions) == 0:
            # This request did not come from one of our authorized proxies, the current IP is the Client.
            log.warning(f"Return {outmost_proven_ip}, since it is not a proxy.")
            break

        proxy_definition, = matching_reverse_proxy_definitions

        proxy_definition: ReverseProxy

        header_definition = proxy_definition.header_added

        if header_definition.uppercase_name not in headers.keys():
            warn("This request came from a reverse proxy, but the proxy added no header."
                 " This might be due to other programs on the same host, or due to malconfiguration,"
                 " both being a potential risk")
            log.warning(f"Return {outmost_proven_ip}, since the proxy did not set its header.")
            break

        new_address = _parse_and_update_header(header_definition, headers)
        log.warning(f"Trusted proxy {outmost_proven_ip} saw address {new_address} and wrote it to header {header_definition.uppercase_name}")

        assert new_address is not None

        outmost_proven_ip = new_address

        continue

    return outmost_proven_ip


def _parse_and_update_header(header_definition, headers):
    field_name = header_definition.uppercase_name
    field_value = headers[field_name]
    field_value: str
    # Comma-separation is specified in https://www.w3.org/Protocols/rfc2616/rfc2616-sec4.html#sec4.2
    values = field_value.split(",")

    if header_definition.order == Order.HEADER_PREPENDED:
        potential_address = values.pop(0)
    elif header_definition.order == Order.HEADER_APPENDED:
        potential_address = values.pop() # default: last
    else:
        raise Exception("Invalid definition of header insertion")

    # reconstruct the request as it should have looked before the current reverse proxy added the header
    if values:
        field_value = ",".join(values)
        headers[field_name] = field_value
    else:
        headers.pop(field_name)

    potential_address = potential_address.strip()

    parser = header_definition.custom_parser
    if parser:
        new_address = parser(potential_address)
    else:
        new_address = ip_address(potential_address)
    return new_address


def _get_matching_proxy_definitions(outmost_proven_ip, proxies):
    matching_reverse_proxies = []
    log.warning(proxies)
    for proxy in proxies:
        proxy: ReverseProxy
        for ip_network in proxy.ip_networks:
            log.warning(f"{outmost_proven_ip} is in {ip_network}: {outmost_proven_ip in ip_network}")
            if outmost_proven_ip in ip_network:
                matching_reverse_proxies.append(proxy)
    return matching_reverse_proxies

from enum import Enum, auto
from typing import List, Union, Callable
from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network, ip_network, ip_address
from warnings import warn


class Order(Enum):
    HEADER_APPENDED = auto()
    HEADER_PREPENDED = auto()


class Header:
    def __init__(self,
                 name: str,
                 order:Order=Order.HEADER_APPENDED,
                 custom_parser: Callable[[str], Union[IPv4Address, IPv6Address]] = None
                 ):
        self.custom_parser = custom_parser
        self.order = order
        # header field names are case insensitive
        # https://datatracker.ietf.org/doc/html/rfc7230#section-3.2
        # we convert them to uppercase now to avoid different parts of code matching differenly;
        # if this breaks anything, the remainder of the code is broken.
        self.uppercase_name = name.upper()


class ReverseProxy:
    def __init__(self,
                 header_added: Header,
                 *ip_addresses: Union[str, IPv4Address, IPv4Network, IPv6Address, IPv6Network],
                 ):
        """
        :param ip_addresses: You can use anything that ipaddress.ip_network accepts, e.g. `127.0.0.0/8` or `::1`
        :param headers_added: Specify here which header this host adds. We only support one header per reverse proxy
        """

        if not ip_addresses:
            warn("A reverse proxy configuration without IP addresses will be ignored.")

        self.header_added = header_added
        ip_networks = []
        for address in ip_addresses:
            # Addresses will be converted to /32 resp. /128 networks, matching exactly one IP
            ip_networks.append(ip_network(address))
        self.ip_networks = ip_networks

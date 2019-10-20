from django.conf import settings


# Search for the real IP address in the following order
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Forwarded-For
# X-Forwarded-For: <client>, <proxy1>, <proxy2>
# Configurable via settings.py
IPWARE_META_PRECEDENCE_ORDER = getattr(settings,
    'IPWARE_META_PRECEDENCE_ORDER', (
        'HTTP_X_FORWARDED_FOR', 'X_FORWARDED_FOR',
        'HTTP_CLIENT_IP',
        'HTTP_X_REAL_IP',
        'HTTP_X_FORWARDED',
        'HTTP_X_CLUSTER_CLIENT_IP',
        'HTTP_FORWARDED_FOR',
        'HTTP_FORWARDED',
        'HTTP_VIA',
        'REMOTE_ADDR',
    )
)

# Private IP addresses
# http://en.wikipedia.org/wiki/List_of_assigned_/8_IPv4_address_blocks
# https://en.wikipedia.org/wiki/Reserved_IP_addresses
# https://www.ietf.org/rfc/rfc1112.txt (IPv4 multicast)
# http://www.ietf.org/rfc/rfc3330.txt (IPv4)
# http://www.ietf.org/rfc/rfc5156.txt (IPv6)
# https://www.ietf.org/rfc/rfc6890.txt
# Regex would be ideal here, but this is keeping it simple
# Configurable via settings.py
IPWARE_PRIVATE_IP_PREFIX = getattr(settings,
    'IPWARE_PRIVATE_IP_PREFIX', (
        '0.0.0.0/8',  # messages to software
        '10.0.0.0/8',  # class A private block
        '100.64.0.0/10',  # carrier-grade NAT
        '169.254.0.0/16',  # link-local block
        '172.16.0.0/12',  # class B private blocks
        '192.0.0.0/24',  # reserved for IANA special purpose address registry
        '192.0.2.0/24',  # reserved for documentation and example code
        '192.168.0.0/16',  # class C private block
        '198.18.0.0/15',  # reserved for inter-network communications between two separate subnets
        '198.51.100.0/24',  # reserved for documentation and example code
        '203.0.113.0/24',  # reserved for documentation and example code
        '224.0.0.0/4',  # multicast
        '240.0.0.0/4',  # reserved
    ) + (
        '::/128',  # Unspecified address
        '::ffff:0:0/96',  # IPv4 mapped addresses
        '::ffff:0:0:0/96',  # IPv6 translated addresses
        '100::/64',  # routing
        '2001:20::/28',  # ORCHIDv2
        '2001:db8::/32',  # reserved for documentation and example code
        'fc00::/7',  # IPv6 private block
        'fe80::/10',  # link-local unicast
        'ff00::/8',  # IPv6 multicast
    )
)

IPWARE_LOOPBACK_PREFIX = (
    '127.0.0.0/8',  # IPv4 loopback device (Host)
    '::1/128',  # IPv6 loopback device (Host)
)

IPWARE_NON_PUBLIC_IP_PREFIX = IPWARE_PRIVATE_IP_PREFIX + IPWARE_LOOPBACK_PREFIX

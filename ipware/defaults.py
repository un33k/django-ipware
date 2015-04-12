from django.conf import settings


# Header that proxy servers for this Django instance
# use to convey the IP address of the client issuing
# the request.
IPWARE_META_IP_ADDRESS_HEADER = getattr(settings, 'IPWARE_META_IP_ADDRESS_HEADER', None)

# Search for the real IP address in the following order
# Configurable via settings.py
IPWARE_META_PRECEDENCE_ORDER = getattr(settings,
    'IPWARE_META_PRECEDENCE_ORDER', (
        'HTTP_X_FORWARDED_FOR',  # client, proxy1, proxy2
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
# http://www.ietf.org/rfc/rfc3330.txt (IPv4)
# http://www.ietf.org/rfc/rfc5156.txt (IPv6)
# Regex would be ideal here, but keeping it simple
# as this is configurable via settings.py
IPWARE_PRIVATE_IP_PREFIX = getattr(settings,
    'IPWARE_PRIVATE_IP_PREFIX', (
        '0.', '1.', '2.',  # externally non-routable
        '10.',  # class A private block
        '169.254.',  # link-local block
        '172.16.', '172.17.', '172.18.', '172.19.',
        '172.20.', '172.21.', '172.22.', '172.23.',
        '172.24.', '172.25.', '172.26.', '172.27.',
        '172.28.', '172.29.', '172.30.', '172.31.',  # class B private blocks
        '192.0.2.',  # reserved for documentation and example code
        '192.168.',  # class C private block
        '255.255.255.',  # IPv4 broadcast address
    ) + (  # the following addresses MUST be in lowercase)
        '2001:db8:',  # reserved for documentation and example code
        'fc00:',  # IPv6 private block
        'fe80:',  # link-local unicast
        'ff00:',  # IPv6 multicast
    )
)

IPWARE_NON_PUBLIC_IP_PREFIX = IPWARE_PRIVATE_IP_PREFIX + (
    '127.',  # IPv4 loopback device
    '::1',  # IPv6 loopback device
)

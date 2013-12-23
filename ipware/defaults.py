from django.conf import settings


# Search for the real IP address in the following order
IPWARE_META_PRECEDENCE_LIST = getattr(settings,
    'IPWARE_META_PRECEDENCE_LIST', (
        'HTTP_X_FORWARDED_FOR', # client, proxy1, proxy2 (set by: Proxy or LB)
        'HTTP_X_REAL_IP', # client (set by: Proxy or LB)
        'REMOTE_ADDR', # client (direct connection)
    )
)

# List of private IP address range (lowercase)
# (http://www.ietf.org/rfc/rfc3330.txt)
IPWARE_PRIVATE_IP_PREFIX = getattr(settings,
    'IPWARE_PRIVATE_IP_PREFIX', (
        '0.', # non-routable or local broadcast
        '10.', # class A private block
        '169.254.', # IPv4 link-local
        '172.16.', '172.31.', # class B private blocks
        '192.0.2.', # examples in documentation
        '192.168.', # class C private block
        '255.', # IPv4 broadcast address
    ) + (
        'fc00:' # IPv6 private block
        'ff00:', # IPv6 multicast
    )
)

IPWARE_NON_PUBLIC_IP_PREFIX = IPWARE_PRIVATE_IP_PREFIX + (
    '127.', # IPv4 loopback device
    '::1', # IPv6 loopback device
)



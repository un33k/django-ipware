from django.conf import settings


IPWARE_META_PRECEDENCE_LIST = getattr(settings,
    'IPWARE_META_PRECEDENCE_LIST',
    ('HTTP_X_FORWARDED_FOR', 'HTTP_X_REAL_IP', 'REMOTE_ADDR',),
)

IPWARE_PRIVATE_IP_PREFIX = getattr(settings,
    'IPWARE_PRIVATE_IP_PREFIX',
    ('10.', '127.', '172.', '192.',) + ('::1',),
)





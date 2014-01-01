Django IPware
====================

**A Django application to retrieve user's IP address**

[![build-status-image-travis]][travis]
[![build-status-image-fury]][fury]
[![build-status-image-pypi]][pypi]


Overview
====================

**Best attempt** to get user's (client's) real ip-address while keeping it **DRY**.

How to install
====================

    1. easy_install django-ipware
    2. pip install django-ipware
    3. git clone http://github.com/un33k/django-ipware
        a. cd django-ipware
        b. run python setup.py
    4. wget https://github.com/un33k/django-ipware/zipball/master
        a. unzip the downloaded file
        b. cd into django-ipware-* directory
        c. run python setup.py


How to use
====================

    # If your web server is publicly accessible on the Internet
    # =========================================================
    # To get the `real`, `public` IP address of the client.
    # Where:
    #    `Real IP` = Client's IP and not that of any `in-between` proxies.
    #    `Public IP` = Any IP address that is route-able on the Internet

    from ipware.ip import get_real_ip
    ip = get_real_ip(request)
    if ip is not None:
       # we have a real, public ip address for user
    else:
       # we don't have a real, public ip address for user


    # If your web server is NOT publicly accessible on the Internet
    # =============================================================
    # To get the `best matched` IP address of the client.
    # Where:
    #    `Best Matched IP` = The first matched public IP or the last matched non-public IP.

    from ipware.ip import get_ip
    ip = get_ip(request)
    if ip is not None:
       # we have an ip address for user
    else:
       # we don't have an ip address for user


Advanced users:
====================

    # you can provide your own meta precedence order by
    # including IPWARE_META_PRECEDENCE_ORDER in your
    # settings.py. The check is done from top to bottom
    IPWARE_META_PRECEDENCE_LIST = (
        'HTTP_X_FORWARDED_FOR', # client, proxy1, proxy2
        'HTTP_CLIENT_IP',
        'HTTP_X_REAL_IP',
        'HTTP_X_FORWARDED',
        'HTTP_X_CLUSTER_CLIENT_IP',
        'HTTP_FORWARDED_FOR',
        'HTTP_FORWARDED',
        'HTTP_VIA',
        'REMOTE_ADDR',
    )

    # you can provide your own private IP prefixes by
    # including IPWARE_PRIVATE_IP_PREFIX in your setting.py
    # IPs that start with items listed below are ignored
    # and are not considered a `real` IP address
    IPWARE_PRIVATE_IP_PREFIX = (
        '0.', '1.', '2.', # externally non-routable
        '10.', # class A private block
        '169.254.', # link-local block
        '172.16.', '172.17.', '172.18.', '172.19.',
        '172.20.', '172.21.', '172.22.', '172.23.',
        '172.24.', '172.25.', '172.26.', '172.27.',
        '172.28.', '172.29.', '172.30.', '172.31.', # class B private blocks
        '192.0.2.', # reserved for documentation and example code
        '192.168.', # class C private block
        '255.255.255.', # IPv4 broadcast address
    ) + (  # the following addresses MUST be in lowercase)
        '2001:db8:', # reserved for documentation and example code
        'fc00:', # IPv6 private block
        'fe80:', # link-local unicast
        'ff00:', # IPv6 multicast
    )


Running the tests
====================

To run the tests against the current environment:

    python manage.py test


License
====================

Protected by ([BSD](LICENSE.md))


[build-status-image-travis]: https://secure.travis-ci.org/un33k/django-ipware.png?branch=master
[travis]: http://travis-ci.org/tomchristie/django-ipware?branch=master

[build-status-image-fury]: https://badge.fury.io/py/django-ipware.png
[fury]: http://badge.fury.io/py/django-ipware

[build-status-image-pypi]: https://pypip.in/d/django-ipware/badge.png
[pypi]: https://crate.io/packages/django-ipware?version=latest


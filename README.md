Django IPware
====================

**A Django application to retrieve user's IP address**

**Author:** Val Neekman, [ info@neekware.com, [@vneekman](https://twitter.com/vneekman) ]

Overview
========

`Best attempt` to get user's (client's) real ip-address


How to install
==================

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
=================
    # if you want the real IP address
    from ipware.ip import get_real_ip
    ip = get_real_ip(request)
    if ip is not None:
       # we have a real ip address for user
    else:
       # we don't have a real ip address for user

    # if you want the best matched IP address
    from ipware.ip import get_ip
    ip = get_ip(request)
    if ip is not None:
       # we have an ip address for user
    else:
       # we don't have an ip address for user

Advanced users:
=================
    # you provide your own meta precedence order by
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
)


Running the tests
=================

To run the tests against the current environment:

    python manage.py test


License
=======

Copyright © Val Neekman ([Neekware Inc.](http://neekware.com))

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this
list of conditions and the following disclaimer in the documentation and/or
other materials provided with the distribution.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


Note: Django is a registered trademark of the Django Software Foundation.




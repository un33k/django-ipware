# (Yet Another?) Django IPware

**A Django application to retrieve client's IP address**

[![status-image]][status-link]
[![version-image]][version-link]
[![coverage-image]][coverage-link]

# Rationale

In contrast to django-ipware as of 3.0.7 / 4.0.0, this fork tries to avoid unsecure guessing IP addresses.

django-ipware 3.0.7 / 4.0.0, when used with multiple headers, allows injecting forged IPs via additional headers set by the client.
Confusion between underscore and dash might allow to circumvent security measures.

To be able to determine in client's IP address in a verifiable way, it requires more configuration,
to get the necessary knowledge of your network setup.

# Notice

**THIS LIBRARY'S CONFIGURATION AND API IS INCOMPATIBLE WITH DJANGO-IPWARE.**

# Configuration

Configure all trustworthy proxies. Note that at most one proxy can be hosted at any IP, do not run different proxies 
adding different headers on the same machine.

```python
IPWARE_REVERSE_PROXIES=[
    ReverseProxy(Header("X-Forwarded-For"), "127.0.0.1"),
    ReverseProxy(Header("X-Forwarded-For"), "127.0.0.0/8"),
    ReverseProxy(Header("X-Forwarded-For"), "::1"),
    ReverseProxy(Header("X-Forwarded-For"), "10.11.12.0/24"),
    ReverseProxy(Header("X-Forwarded-For"), "fd8a:dfe1:9c30:dbfc::/64"),
    # for proxies prepending headers instead of appending them, use:
    ReverseProxy(Header("X-Forwarded-For", order=Order.HEADER_PREPENDED), "127.0.0.1"),
]


```

Headers are expected to only contain the ip address and some whitespace. IPv6 addresses should be written without brackets.

The order of the IP addresses is not checked; and of those trustworthy hosts might forge any client IP address anyway.
This allows you to add more IP addresses for clustering.

# Security

IP address spoofing and MITM is out of scope; this Django library trusts every IP address it or any authorized reverse proxy sees.

Consider reverse path filtering and network segmentation, and make sure you don't reuse whitelisted IPs in your network.

# How to install

TODO 

    1. easy_install django-ipware
    2. pip install django-ipware
    3. git clone http://github.com/un33k/django-ipware
        a. cd django-ipware
        b. run python setup.py install
    4. wget https://github.com/un33k/django-ipware/zipball/master
        a. unzip the downloaded file
        b. cd into django-ipware-* directory
        c. run python setup.py install

# How to use

```python
 # In a view or a middleware where the `request` object is available

 from ipware import get_client_ip
 # This variant of the library will always return an IP (although it might be your proxy's IP), or raise an exception.
 client_ip = get_client_ip(request)
 # We got the client's IP address (as an ipaddress.IPv4Address or IPv6Address object)
 # Note that there is no is_routable anymore. It is too unspecific to be used securely, especially in edge-cases.
 # Alternatives could be:
 client_ip.is_global # internet or global ip addresses of hosts in your own network
 client_ip.is_private # private ip addresses
 client_ip.is_loopback # 127.0.0.1, etc.
 # Consider: there are more IP addresses which are neither, see IANA for a list of assigments.
```

# Running the tests

To run the tests against the current environment:

    python manage.py test

# License

Released under a ([MIT](LICENSE)) license.

# Version

X.Y.Z Version

    `MAJOR` version -- when you make incompatible API changes,
    `MINOR` version -- when you add functionality in a backwards-compatible manner, and
    `PATCH` version -- when you make backwards-compatible bug fixes.

[status-image]: https://travis-ci.org/un33k/django-ipware.svg?branch=master
[status-link]: https://travis-ci.org/un33k/django-ipware
[version-image]: https://img.shields.io/pypi/v/django-ipware.svg
[version-link]: https://pypi.python.org/pypi/django-ipware
[coverage-image]: https://coveralls.io/repos/un33k/django-ipware/badge.svg
[coverage-link]: https://coveralls.io/r/un33k/django-ipware
[download-image]: https://img.shields.io/pypi/dm/django-ipware.svg
[download-link]: https://pypi.python.org/pypi/django-ipware

# Sponsors

[Neekware Inc.](http://neekware.com)

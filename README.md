# Django IPware 

**A Django application to retrieve client's IP address**

[![status-image]][status-link]
[![version-image]][version-link]
[![coverage-image]][coverage-link]

# Alternative package

If you prefer a python only version that does not integrate with Django directly, but allows for more flexibility and advanced features, you can use the [python-ipware](https://github.com/un33k/python-ipware) package instead.  `django-ipware` is a wrapper using [python-ipware](https://github.com/un33k/python-ipware) under the hood staring from version `6.0.0`.

# Overview

**Best attempt** to get client's IP address while keeping it **DRY**.

# Notice

There is no perfect `out-of-the-box` solution against fake IP addresses, aka `IP Address Spoofing`.
You are encouraged to read the ([Advanced users](README.md#advanced-users)) section of this page and
use `trusted_proxies_ips` and/or `proxy_count` features to match your needs, especially `if` you are
planning to include `ipware` in any authentication, security or `anti-fraud` related architecture.

This is an open source project, with the source code visible to all. Therefore, it may be exploited through unimplemented, or improperly implemented features.

Please use ipware `ONLY` as a complement to your `firewall` security measures!

# How to install

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
 client_ip, is_routable = get_client_ip(request)
 if client_ip is None:
    # Unable to get the client's IP address
 else:
     # We got the client's IP address
     if is_routable:
         # The client's IP address is publicly routable on the Internet
     else:
         # The client's IP address is private
```

# Advanced users:

- ### Precedence Order

  The default meta precedence order is top to bottom. You may customize the order
  by providing your own `IPWARE_META_PRECEDENCE_ORDER` by adding it to your project's settings.py

  ```python
   # The default meta precedence order (update as needed)
   IPWARE_META_PRECEDENCE_ORDER = (
        "X_FORWARDED_FOR",  # AWS ELB (default client is `left-most` [`<client>, <proxy1>, <proxy2>`])
        "HTTP_X_FORWARDED_FOR",  # Similar to X_FORWARDED_TO
        "HTTP_CLIENT_IP",  # Standard headers used by providers such as Amazon EC2, Heroku etc.
        "HTTP_X_REAL_IP",  # Standard headers used by providers such as Amazon EC2, Heroku etc.
        "HTTP_X_FORWARDED",  # Squid and others
        "HTTP_X_CLUSTER_CLIENT_IP",  # Rackspace LB and Riverbed Stingray
        "HTTP_FORWARDED_FOR",  # RFC 7239
        "HTTP_FORWARDED",  # RFC 7239
        "HTTP_VIA",  # Squid and others
        "X-CLIENT-IP",  # Microsoft Azure
        "X-REAL-IP",  # NGINX
        "X-CLUSTER-CLIENT-IP",  # Rackspace Cloud Load Balancers
        "X_FORWARDED",  # Squid
        "FORWARDED_FOR",  # RFC 7239
        "CF-CONNECTING-IP",  # CloudFlare
        "TRUE-CLIENT-IP",  # CloudFlare Enterprise,
        "FASTLY-CLIENT-IP",  # Firebase, Fastly
        "FORWARDED",  # RFC 7239
        "CLIENT-IP",  # Akamai and Cloudflare: True-Client-IP and Fastly: Fastly-Client-IP
        "REMOTE_ADDR",  # Default
    )
  ```

  **Alternatively**, you can provide your custom _request header meta precedence order_ when calling `get_client_ip()`.

```python
get_client_ip(request, request_header_order=['X_FORWARDED_FOR'])
get_client_ip(request, request_header_order=['X_FORWARDED_FOR', 'HTTP_X_FORWARDED_FOR'])
```

- ### Proxy Count

  The default meta proxy count is 0 unless explictly provided as an argument to `get_client_ip()`. You may customize the order
  by providing your own `IPWARE_META_PROXY_COUNT` by adding it to your project's settings.py

### Trusted Proxies

If your Django server is behind one or more known proxy server(s), you can filter out unwanted requests
by providing the `trusted` proxy list when calling `get_client_ip(request, proxy_trusted_ips=['177.139.233.133'])`.
In the following example, your load balancer (LB) can be seen as a `trusted` proxy.

```
 `Real` Client  <public> <---> <public> LB (Server) <private> <--------> <private> Django Server
                                                                   ^
                                                                   |
 `Fake` Client  <private> <---> <private> LB (Server) <private> ---^
```

```python
# In the above scenario, use your load balancer IP address as a way to filter out unwanted requests.
client_ip, is_routable = get_client_ip(request, proxy_trusted_ips=['177.139.233.133'])

# If you have multiple proxies, simply add them to the list
client_ip, is_routable = get_client_ip(request, proxy_trusted_ips=['177.139.233.133', '177.139.233.134'])

# For proxy servers with fixed sub-domain and dynamic IP, use the following pattern.
client_ip, is_routable = get_client_ip(request, proxy_trusted_ips=['177.139.', '177.140'])
client_ip, is_routable = get_client_ip(request, proxy_trusted_ips=['177.139.233.', '177.139.240'])
```

`Please note:` By default, the `right-most` proxy in the chain is the `trusted` proxy and that is the one your django
server talks to. Therefore, `ipware` checks to see if the `right-most` proxy address starts with any ip pattern that was
passed in via the `proxy_trusted_ips` list.

### Proxy Count

If your Django server is behind a `known` number of proxy server(s), you can filter out unwanted requests
by providing the `number` of proxies when calling `get_client_ip(request, proxy_count=1)`.
In the following example, your load balancer (LB) can be seen as the `only` proxy.

```
 `Real` Client  <public> <---> <public> LB (Server) <private> <--------> <private> Django Server
                                                                   ^
                                                                   |
                                       `Fake` Client  <private> ---^
```

```python
# In the above scenario, the total number of proxies can be used as a way to filter out unwanted requests.
client_ip, is_routable = get_client_ip(request, proxy_count=1)

# The above may be very useful in cases where your proxy server's IP address is assigned dynamically.
# However, If you have the proxy IP address, you can use it in combination to the proxy count.
client_ip, is_routable = get_client_ip(request, proxy_count=1, proxy_trusted_ips=['177.139.233.133'])
```

### Originating Request

If your proxy server is configured such that the right-most IP address is that of the originating client, you
can indicate `right-most` as your `proxy_order` when calling `get_client_ip(request, proxy_order="right-most")`.
Please note that the [de-facto](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Forwarded-For) standard
for the originating client IP address is the `left-most` as per `<client>, <proxy1>, <proxy2>`.

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

[status-image]: https://github.com/un33k/django-ipware/actions/workflows/ci.yml/badge.svg
[status-link]: https://github.com/un33k/django-ipware/actions/workflows/ci.yml
[version-image]: https://img.shields.io/pypi/v/django-ipware.svg
[version-link]: https://pypi.python.org/pypi/django-ipware
[coverage-image]: https://coveralls.io/repos/un33k/django-ipware/badge.svg
[coverage-link]: https://coveralls.io/r/un33k/django-ipware

# Sponsors

[Neekware Inc.](http://neekware.com)

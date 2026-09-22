# Django IPware

**A Django application to retrieve a client's real IP address**

[![status-image]][status-link]
[![version-image]][version-link]
[![coverage-image]][coverage-link]

`django-ipware` is a thin Django wrapper around [python-ipware](https://github.com/un33k/python-ipware),
which does the actual work. If you don't use Django, or want the full API (such as the `trusted_route`
flag), use python-ipware directly.

# Notice

There is no perfect `out-of-the-box` solution against fake IP addresses, aka `IP Address Spoofing`.
Read the [Advanced users](#advanced-users) section and use `proxy_trusted_ips` and/or `proxy_count`,
especially if you use `ipware` in any authentication, security or anti-fraud related architecture.

Please use ipware `ONLY` as a complement to your `firewall` security measures!

# How to install

    pip install django-ipware

Requires Python 3.10+ and Django 5.2+. For older Python or Django versions, use `django-ipware<8`.

# How to use

```python
# In a view or a middleware where the `request` object is available

from ipware import get_client_ip

client_ip, is_routable = get_client_ip(request)
if client_ip is None:
    # Unable to get the client's IP address
    ...
else:
    # We got the client's IP address
    if is_routable:
        # The client's IP address is publicly routable on the Internet
        ...
    else:
        # The client's IP address is private
        ...
```

`client_ip` is a string such as `"177.139.233.139"` or `"2606:4700::1"`, or `None`.

# How the IP is chosen

The default algorithm is python-ipware's **modern** engine:

- Headers are checked in order. The first **public** IP wins; otherwise the best private,
  then link-local, then loopback address. Multicast, `0.0.0.0` and reserved addresses are
  never returned.
- Without proxy settings, the first public entry in a chain wins, so
  `X-Forwarded-For: 10.0.0.1, 177.139.233.139` yields `177.139.233.139`.
- RFC 7239 `Forwarded` headers, bracketed IPv6 with ports, IPv4-mapped and NAT64 addresses
  are understood. Malformed values are rejected rather than guessed at.

See python-ipware's [README](https://github.com/un33k/python-ipware#readme) for the full rules and the
default header order.

## Legacy (7.x) behavior

django-ipware 7.x results are available unchanged:

```python
get_client_ip(request, algorithm="legacy")
```

or for the whole project, in `settings.py`:

```python
IPWARE_ALGORITHM = "legacy"
```

The legacy algorithm is frozen and takes no further changes.

# Advanced users

## Arguments

```python
get_client_ip(
    request,
    proxy_order="left-most",     # or "right-most"
    proxy_count=None,            # expected number of proxies in front of Django
    proxy_trusted_ips=None,      # list of trusted proxies
    request_header_order=None,   # header keys to check, in order
    strict=None,                 # strict chain validation; default True
    algorithm=None,              # "auto" (modern), "modern" or "legacy"
)
```

An invalid value raises `ValueError`: an unknown `proxy_order` or `algorithm`, a trusted proxy list
passed as a bare string, an empty or non-IP entry, a negative `proxy_count`, and so on.

## Settings

Each setting applies only when the matching argument is not passed. **An explicit argument always wins.**

| Setting | Argument | Default |
| --- | --- | --- |
| `IPWARE_ALGORITHM` | `algorithm` | `"auto"` (modern) |
| `IPWARE_META_PRECEDENCE_ORDER` | `request_header_order` | python-ipware's default order |
| `IPWARE_META_PROXY_COUNT` | `proxy_count` | not enforced |
| `IPWARE_STRICT` | `strict` | `True` |

```python
# settings.py: behind Cloudflare only
IPWARE_META_PRECEDENCE_ORDER = ("HTTP_CF_CONNECTING_IP", "REMOTE_ADDR")
```

Only put a CDN header first when **all** traffic comes through that CDN; clients can send these headers
themselves.

## Trusted proxies

If Django sits behind known proxies, pass them; requests that did not come through them are rejected:

```python
client_ip, is_routable = get_client_ip(request, proxy_trusted_ips=["177.139.233.133"])
client_ip, is_routable = get_client_ip(request, proxy_trusted_ips=["177.139.233.133", "177.139.233.134"])
client_ip, is_routable = get_client_ip(request, proxy_trusted_ips=["177.139.", "177.140"])  # prefixes
client_ip, is_routable = get_client_ip(request, proxy_trusted_ips=["100.64.0.0/10"])  # CIDR
```

Each entry is a **complete IP** (matched exactly), a **CIDR network**, or an **IP prefix** matched on
whole octets (`"10.1"` matches `10.1.x.x`, not `10.100.x.x`). Prefer CIDR for IPv6.

```
 `Real` Client  <public> <---> <public> LB (Server) <private> <--------> <private> Django Server
                                                                   ^
                                                                   |
 `Fake` Client  <private> <---> <private> LB (Server) <private> ---^
```

## Proxy count

If Django sits behind a known number of proxies:

```python
client_ip, is_routable = get_client_ip(request, proxy_count=1)

# Combine with the proxy's address when you know it:
client_ip, is_routable = get_client_ip(request, proxy_count=1, proxy_trusted_ips=["177.139.233.133"])
```

With `strict=True` (the default) the chain must contain exactly that many proxies; with
`strict=False`, at least that many.

## Strict mode

By default a malformed entry anywhere in a header (for example `unknown, 177.139.233.139`) makes that
header untrusted, and the next header is checked. Pass `strict=False`, or set `IPWARE_STRICT = False`,
to skip bad entries instead.

## Originating request

If your proxy puts the originating client on the right, use `proxy_order="right-most"`. The
[de facto](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Forwarded-For) standard is
`left-most`: `<client>, <proxy1>, <proxy2>`.

# Running the tests

    pip install -e ".[test]"
    python manage.py test

The suite runs the modern default, the legacy algorithm, and the original 7.x tests against both.

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

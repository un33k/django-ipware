# django-ipware 8.0.0

django-ipware is now a thin Django wrapper over
[python-ipware 4.1](https://github.com/un33k/python-ipware), and uses its **modern** engine by default.
`from ipware import get_client_ip` and `get_client_ip(request)` work unchanged.

## Upgrade in one minute

- **Python 3.10+ and Django 5.2+** are required. On older versions, pin `django-ipware<8`.
- **Need exactly the 7.x results?** Set `IPWARE_ALGORITHM = "legacy"` in `settings.py`, or pass
  `algorithm="legacy"`. The legacy algorithm is frozen.
- **Arguments now beat settings.** In 7.x, `IPWARE_META_PRECEDENCE_ORDER` and `IPWARE_STRICT` silently
  overrode the matching arguments. If you relied on that, remove the argument or the setting.
- **`IPWARE_META_PROXY_COUNT` works again.** If it is in your settings, it is now enforced.
- **Trusted proxies are stricter.** A complete IP in `proxy_trusted_ips` matches exactly; it no longer
  also matches longer addresses such as `1.2.3.45` for `"1.2.3.4"`. Use a CIDR or a prefix if you
  relied on that.
- **Misconfiguration raises `ValueError`**, e.g. an unknown `proxy_order`, a bare string for
  `proxy_trusted_ips`, or an empty entry.

## What's better

- A better client IP: public > private > link-local > loopback, the first public hop of a chain, and
  multicast / `0.0.0.0` / reserved addresses are never returned.
- RFC 7239 `Forwarded`, NAT64 and IPv4-mapped addresses understood; malformed values rejected.
- `is_routable` follows python-ipware's ranking.
- New: `strict=False` / `IPWARE_STRICT` (#122), `py.typed` shipped (#124), correct `Optional[str]`
  return type (#126).

## Quality

The original 7.x tests pass on both algorithms. Option-matrix tests check the modern path against
python-ipware's modern engine and the legacy path against its v3 engine, with 100% line and branch
coverage. CI covers Python 3.10–3.14 with Django 5.2, 6.0 and 6.1.

## Thanks

@hirotasoshu (#121, #122), @streadway (#124), @philipstarkey (#125), @btruhand (#126), @sujh (#127).

Full details: [CHANGELOG.md](https://github.com/un33k/django-ipware/blob/master/CHANGELOG.md).

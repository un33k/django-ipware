# 8.0.0

Built on python-ipware 4.1. The default algorithm is now python-ipware's modern engine; the 7.x
behavior stays available, frozen, via `algorithm="legacy"` or `IPWARE_ALGORITHM = "legacy"`.

Community (thank you!):
- Non-strict mode: `get_client_ip(request, strict=False)` or `IPWARE_STRICT = False`. By @hirotasoshu
  (#122, closes #121).
- `py.typed` is shipped in the package, so type checkers see the annotations. By @streadway (#124).
- CI tests currently supported Python and Django versions. By @philipstarkey (#125).
- Return type is `Tuple[Optional[str], bool]`. Reported by @btruhand (#126).
- `IPWARE_META_PROXY_COUNT` works again. Reported by @sujh (#127).

Enhance:
- New `algorithm` argument and `IPWARE_ALGORITHM` setting: `"modern"` (default) or `"legacy"`. Upgrade
  and pass nothing to get modern; set `IPWARE_ALGORITHM = "legacy"` to keep the exact 7.x results.
- Modern picks a better client IP, see python-ipware 4.1: public > private > link-local > loopback,
  the first public hop of a chain, never multicast / `0.0.0.0` / reserved, RFC 7239 `Forwarded`,
  NAT64 unwrapping, and malformed values rejected instead of truncated.
- `is_routable` is True only for globally routable addresses as ranked by python-ipware (deprecated
  site-local `fec0::/10` is no longer reported as routable).
- Trusted proxies: a complete IP matches exactly (7.x prefix-matched, so `"1.2.3.4"` also trusted
  `1.2.3.45`); prefixes match on whole octets; CIDR networks are supported.

Fix:
- An explicit argument now always wins over its Django setting. In 7.x, `IPWARE_META_PRECEDENCE_ORDER`
  and `IPWARE_STRICT` silently overrode the `request_header_order` and `strict` arguments.
- `IPWARE_META_PROXY_COUNT` is read again (documented but ignored in 7.x). It applies only when set.
- `proxy_order` must be `"left-most"` or `"right-most"`; anything else raises `ValueError` (7.x
  silently used right-most).
- Misconfiguration raises `ValueError`, e.g. `proxy_trusted_ips` passed as a bare string, an empty or
  non-IP entry, or a negative `proxy_count`.
- One-shot iterables (generators) work for `proxy_trusted_ips` and `request_header_order`.

Modernize:
- Requires Python 3.10+ and Django 5.2+ (tested on Python 3.10–3.14, Django 5.2, 6.0, 6.1). Django
  4.2 and Python 3.9 are end of life; use `django-ipware<8` for them.
- Depends on `python-ipware>=4.1.0,<5` and declares `Django>=5.2`.
- Packaging moved to PEP 621 `pyproject.toml` with the Hatchling backend; `setup.py` removed.
- CI runs only on pull requests into master: tests on every Python / Django combination, then build.
- Removed the obsolete `default_app_config`.
- Tests: the original 7.x suite runs against both algorithms; option-matrix tests check modern
  against python-ipware's modern engine and legacy against its v3 engine; 100% line and branch coverage.

# 7.0.0 / 7.0.1

Enhance:
- Up version python-ipware (minimal possible api / compatibility change)

# 6.0.5

Enhance:
- Add `HTTP_CF_CONNECTING_IP` to list of known ip headers (Adam M.)
- Remove `HTTP_VIA` header support (unreliable IP information) (@yourcelf)
- Up-version python-ipware to 2.0.3

# 6.0.4

Enhancement:
- Add typings (thx: @federicobond)

# 6.0.3

Enhancement:
- Show in Pypi Python 3.12 is supported (thx: @jrobichaud)

# 6.0.2

Enhancement:
- Add support for Django 5.0 (thx: @cclauss)
- Add support for Python 3.12 (thx: @cclauss)

# 6.0.1

Enhancement:
- Add IPWARE_META_PROXY_COUNT setting + corresponding docs (thx: @mmcclelland1002)

# 6.0.0

Enhancement: (breaking changes)

- Use python-ipware under the hood
- Minor behavior changes as python-ipware is more accurate
- Use 5.0.2 if you need the old behavior

# 5.0.2

Enhancement:

- Drop Python 3.7 support
- Add support for Django 4.2
- Drop support for Django 4.0
- Drop support for PyPy
- Readme updates to encourage users to use `python-ipware` instead of `django-ipware` (thx: rposborne)

# 5.0.0

Enhancement:

- Added support for Python 3.11 (@ccluass - thx)
- Drop support for Python 3.6, Django 2.2

# 4.0.2

Enhancement:

- Added support for Python 3.10 (Thx joshuadavidthomas)

## 4.0.1

Enhancement:

- Added test for django 4.0 (Thx PetrDlouhy)

## 4.0.0

Enhancement:

- Added test to cover more proxy scenarios (thx: Phillip Kuhrt)
- Up versioned major version number as some scenarios have changed

## 3.0.4 / 3.0.5 / 3.0.6 / 3.0.7

Enhancement:

- Clean ups

## 3.0.3

Enhancement:

- Add support for github action (@awais786)

## 3.0.2

Enhancement:

- Add support for ppc64le (@kishorkunal-raj)

## 3.0.1

Fix:

- Ensure no-required build artifacts won't get into the package

## 3.0.0

Enhancement:

- Remove deprecated logic
- Drop "official" support for py < 3.5
- Update to latest Django

## 2.1.1

Enhancement:

- Added deprecation warnings preparing for version 3.0
- Update to latest Django

## 2.1.0

Enhancement:

- Added more non-routable ip blocks (@wking)

## 2.0.2

Enhancement:

- Added the ability to private the request precedence order on each call

## 2.0.1

Enhancement:

- Added more private IP blocks to the default list

## 2.0.0

Fix:

- Update Django versions (@illagrenan)
- Update Readme (@sabueso)
- Added proxy count
- Moved version one readme to /docs

## 1.1.6

Fix:

- Fix trusted proxies Right2Left + Test & Bumped Django versions (@felixxm)
- Changed licensing to MIT

## 1.1.5

Feature:

- Added support for trusted proxy configuration

## 1.1.4

Enhancement:

- Added support for proxies with `underscores_in_headers off;`
- Handling hyphen as delimiter - ex: `X-FORWARDED-FOR` instead of `X_FORWARDED_FOR`
- Up version Django version in .travis.yml

## 1.1.3

Fix:

- Fix read me file updating `IPWARE_META_PRECEDENCE_ORDER` reference.

## 1.1.2

Updates:

- Added support for Django 1.8.6 and Python 3.5.
- Dropped support for Django 1.4.x and Python 2.6 and 3.2

## 1.1.1

Enhancement:

- Added support for X_FORWARDED_FOR

## 1.1.0

Enhancement:

- Added support for 1.0.0.0/8 and 2.0.0.0/8 blocks

## 1.0.0

Enhancement:

- Promoting to production grade

## 0.1.1

Enhancement:

- Support for Left2Right or Right2Left Proxy IP Lookup

## 0.1.0

Enhancement:

- pypy support
- PY3.4 support

## 0.0.9

Enhancement:

- Django 1.7 official support
- First non-loopback private IP match is best matched now.

## 0.0.8

Enhancement:

- Django 1.7 support
- PEP8 Compliance
- Bump Alpha to Beta

## 0.0.6

Enhancement:

- Converted print statements to new format. (Python 3.x)
- Replaced deprecated unit test APIs

## 0.0.5

Enhancement:

- Added Python 3.2 and 3.3 support

## 0.0.4

Enhancement:

- Added changelog file
- Added more private ip prefixes

## 0.0.3

Features:

- Added get_ip() to return the best-matched IP
- Removed get_ip_address_from_request()

Bugfixes:

- Expended the private IP range

## 0.0.2

Features:

- IPv6 support
- Added get_real_ip(), the shorter version of get_ip_address_from_request()

## 0.0.1

Features:

- Initial Release

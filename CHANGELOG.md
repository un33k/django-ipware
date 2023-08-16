# Unreleased

Enhancement:

- Drop Python 3.7 support
- Add support for Django 4.2
- Drop support for Django 4.0
- Drop support for PyPy

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

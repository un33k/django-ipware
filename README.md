Django IPware
====================

**A Django IP application **

**Author:** Val Neekman, [ info@neekware.com, @vneekman ]

Overview
========

Find best matched public IP of a client or return the local loopback (127.0.0.1)

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
    from ipware.ip import get_ip_address_from_request
    ip = get_ip_address_from_request(request)

Running the tests
=================

To run the tests against the current environment:

    python manage.py test

Changelog
=========

0.0.1
-----
* Initial Release


License
=======

Copyright © Val Neekman (Neekware Inc.)

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




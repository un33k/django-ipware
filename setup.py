#!/usr/bin/env python
# Learn more: https://github.com/un33k/setup.py
import os
import sys
from codecs import open
from shutil import rmtree

from setuptools import setup

package = 'ipware'
python_requires = ">=3.8"
here = os.path.abspath(os.path.dirname(__file__))

requires = []
test_requirements = []

about = {}
with open(os.path.join(here, package, '__version__.py'), 'r', 'utf-8') as f:
    exec(f.read(), about)

with open('README.md', 'r', 'utf-8') as f:
    readme = f.read()


def status(s):
    print('\033[1m{0}\033[0m'.format(s))


# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish':
    try:
        status('Removing previous builds…')
        rmtree(os.path.join(here, 'dist'))
    except OSError:
        pass

    status('Building Source and Wheel (universal) distribution…')
    os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

    status('Uploading the package to PyPI via Twine…')
    os.system('twine upload dist/*')

    status('Pushing git tags…')
    os.system('git tag v{0}'.format(about['__version__']))
    os.system('git push --tags')
    sys.exit()

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=readme,
    long_description_content_type='text/markdown',
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    packages=[package],
    package_data={'': ['LICENSE']},
    package_dir={'ipware': 'ipware'},
    include_package_data=True,
    python_requires=python_requires,
    install_requires=requires,
    license=about['__license__'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    cmdclass={},
    tests_require=test_requirements,
    extras_require={},
    project_urls={},
)

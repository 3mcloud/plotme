#!/usr/bin/env python
# Based on: https://github.com/kennethreitz/setup.py/blob/master/setup.py
"""
Setup tools
Use setuptools to install package dependencies. Instead of a requirements file you
can install directly from this file.
`pip install .`
You can install test dependencies by targeting the appropriate key in extras_require
```
pip install .[test] # install requires and test requires
```
See: https://packaging.python.org/tutorials/installing-packages/#installing-setuptools-extras
"""
import platform
import re
import subprocess
from pathlib import Path
from setuptools import find_packages, setup


# Package meta-data.
NAME = 'plotme'
DESCRIPTION = 'plot all the things in all the folders automatically but only if there have been changes'
URL = 'https://github.mmm.com/3mcloud/plotme'
EMAIL = 'nikolarobottesla@users.noreply.github.com, dgarcia7654@users.noreply.github.com'
AUTHOR = 'Milo Oien-Rochat, Daniel Garcia'
REQUIRES_PYTHON = '>=3.7.0'
# VERSION set in 1st __init__.py

# What packages are required for this module to be executed?
REQUIRES = [
    'dirhash',
    'numpy',
    'jsonschema',
    'openpyxl',
    'pandas',
    'plotly',
    'scandir'
]

REQUIRES_TEST = [
    'pip',
    'pylint',
    'pytest',
    'pytest-env',
    'pytest-cov'
]

REQUIRES_DEBUG = [

]

# What packages are optional?
EXTRAS = {
    # 'fancy feature': ['django'],
}


def has_ssh() -> bool:
    """
    Check that the user has ssh access to github.mmm.com
    First it will verify if ssh is installed in $PATH
    then check if we can authenticate to github.mmm.com
    over ssh. Returns false if either of these are untrue
    """
    result = None
    if 'windows' in platform.platform().lower():
        ssh_test = subprocess.run(['where', 'ssh'])
    else:
        ssh_test = subprocess.run(['which', 'ssh'])
    if ssh_test.returncode == 0:
        result = subprocess.Popen(
            ['ssh', '-Tq', 'git@github.mmm.com', '&>', '/dev/null'])
        result.communicate()
    if not result or result.returncode == 255:
        return False
    return True


def flip_ssh(requires: list) -> list:
    """
    Attempt to authenticate with ssh to github.mmm.com
    If permission is denied then flip the ssh dependencies
    to https dependencies automatically.
    """
    # Not authenticated via ssh. Change ssh to https dependencies
    if not has_ssh():
        requires = list(map(
            lambda x: re.sub(r'ssh://git@', 'https://', x), requires
        ))
    return requires


def get_property(prop, project):
    """
    get a property from the init.py file
    """
    init_path = str(Path(project, '__init__.py'))
    result = re.search(r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop), open(init_path).read())
    return result.group(1)


setup(
    name=NAME,
    version=get_property('__version__', Path(NAME)),
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(
        where=NAME,
        exclude=[
            "*.tests",
            "*.tests.*"
            "tests.*",
            "tests"
        ]
    ),
    install_requires=flip_ssh(REQUIRES),
    extras_require={
        'test': flip_ssh(REQUIRES_TEST),
        'debug': flip_ssh(REQUIRES_DEBUG)
    },
    include_package_data=False,
    license='UNLICENSED',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)

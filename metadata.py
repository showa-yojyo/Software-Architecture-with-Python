#!/usr/bin/env python

from importlib.metadata import metadata, PackageNotFoundError

PACKAGES = '''
requests
pytest
Selenium
matplotlib
pybloom
profile
objgraph
pympler
aiohttp
async_timeout
celery
Pillow
pymp-pypi
joblib
passlib
Flask
Eventlet
gevent
Django
twisted
Fablic
Schematics
Redis
'''

for package in PACKAGES.splitlines():
    try:
        data = metadata(package)
        name = data['Name']
        url = data['Home-page']
        desc = data['Summary']
        print(f'* [{name}]({url}): {desc}')
    except PackageNotFoundError:
        print(package)

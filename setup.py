#!/usr/bin/python
"""
flask-protorpc
--------------

Protocol Buffers for RESTful interfaces.

http://github.com/gregorynicholas/flask-protorpc
`````

* `documentation <http://packages.python.org/flask-protorpc>`_
* `development version
  <http://github.com/gregorynicholas/flask-protorpc/zipball/master#egg=flask-protorpc-dev>`_

"""
from setuptools import setup

setup(
  name='flask-protorpc',
  version='1.0.0',
  url='http://github.com/gregorynicholas/flask-protorpc',
  license='MIT',
  author='gregorynicholas',
  description='Protocol Buffers for RESTful interfaces.',
  long_description=__doc__,
  packages=['flaskext'],
  namespace_packages=['flaskext'],
  zip_safe=False,
  platforms='any',
  install_requires=['flask'],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development :: Libraries :: Python Modules'
  ]
)

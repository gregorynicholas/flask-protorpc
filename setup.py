#!/usr/bin/python
"""
flask_protorpc
--------------

Protocol Buffers for RESTful interfaces.

http://github.com/gregorynicholas/flask-protorpc
`````

* `documentation <http://packages.python.org/flask_protorpc>`_
* `development version
  <http://github.com/gregorynicholas/flask-protorpc/zipball/master#egg=flask_protorpc-dev>`_

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
  packages=[
  ],
  namespace_packages=[
    'flask_protorpc'
  ],
  py_modules=[
    'flask_protorpc.proto',
  ],
  zip_safe=False,
  platforms='any',
  install_requires=['flask', 'google-protorpc'],
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

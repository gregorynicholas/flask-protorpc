#!/usr/bin/env python
"""
flask_protorpc
--------------

An extremely thin Flask Extension to build remote clients.

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
  description='An extremely thin Flask Extension to build remote clients.',
  long_description=__doc__,
  py_modules=[
    'flask_protorpc',
    'flask_protorpc_tests',
    'testutils',
  ],
  # packages=['flaskext'],
  # namespace_packages=['flaskext'],
  zip_safe=False,
  platforms='any',
  install_requires=[
    'flask==0.9',
    'google-protorpc==1.0.0'
  ],
  dependency_links = [
    'https://github.com/gregorynicholas/google-protorpc/tarball/master',
  ],
  test_suite='flask_protorpc_tests',
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

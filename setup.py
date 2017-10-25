import os
import io
import sys
from setuptools import setup

from webscaff import VERSION


PATH_BASE = os.path.dirname(__file__)

PYTEST_RUNNER = ['pytest-runner'] if 'test' in sys.argv else []


def get_readme():
    # This will return README (including those with Unicode symbols).
    with io.open(os.path.join(PATH_BASE, 'README.rst')) as f:
        return f.read()


setup(
    name='webscaff',
    version='.'.join(map(str, VERSION)),
    url='https://github.com/idlesign/webscaff',

    description='Scaffolding for web applications.',
    long_description=get_readme(),
    license='BSD 3-Clause License',

    author='Igor `idle sign` Starikov',
    author_email='idlesign@yandex.ru',

    packages=['webscaff'],
    include_package_data=True,
    zip_safe=False,

    install_requires=['fabric'],
    setup_requires=[] + PYTEST_RUNNER,
    tests_require=['pytest'],

    test_suite='tests',

    classifiers=[
        # As in https://pypi.python.org/pypi?:action=list_classifiers
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: BSD License'
    ],
)

#!/usr/bin/env python3

from distutils.core import setup
setup(
    name="keyboard",
    version='0.1',
    description="A tone generator with midi support",
    author='Lucas Wilson',
    author_email='lkwilson96@gmail.com',
    url='https://github.com/larkwt96',
    install_requires=['pygame'],
    packages=['keyboard'],
    package_dir={'keyboard': 'src/keyboard'},
    include_package_data=True,
)

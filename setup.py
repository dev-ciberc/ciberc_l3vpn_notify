"""
Setup file for ciberc_l3vpn_notify
"""
from setuptools import find_packages, setup

setup(
    name='ciberc_l3vpn_notify',
    version='0.1',
    description='CiberC Automated Cases',
    author='Rafael Fernando Garcia Sagastume',
    packages=find_packages(exclude=["tests"]),
    package_data={
        'ciberc_l3vpn_notify': [
            'templates/config-templates/*',
            'templates/rollback-templates/*',
            'templates/napalm-process/*',
        ]
    },
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'ciberc-l3vpn = ciberc_l3vpn_notify.main:main'
        ]
    }
)

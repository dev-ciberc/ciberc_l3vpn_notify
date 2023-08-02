"""
Setup file for ciberc_l3vpn_notify
"""
from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setup(
    name='ciberc_l3vpn_notify',
    version='0.1.1',
    description='CiberC Automated Cases',
    author='Rafael Fernando Garcia Sagastume',
    packages=find_packages(exclude=["tests"]),
    package_data={
        'ciberc_l3vpn_notify': [
            'templates/config-templates/*',
            'templates/rollback-templates/*',
        ]
    },
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'ciberc-l3vpn = ciberc_l3vpn_notify.main:main'
        ]
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'nornir==3.3.0',
        'nornir-jinja2==0.2.0',
        'nornir-netmiko==1.0.0',
        'nornir_napalm==0.4.0',
        'nornir_utils==0.2.0',
        'napalm==4.1.0',
        'napalm-huawei-vrp==1.1.0',
        'typer==0.9.0',
        'setuptools==68.0.0',
        'wheel==0.41.0',
        'webexteamsbot==0.1.4.2',
        'tqdm==4.65.0',
        'pylint==2.17.5',
    ],
)

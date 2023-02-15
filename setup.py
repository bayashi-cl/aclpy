# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['atcoder']

package_data = \
{'': ['*']}

install_requires = \
['pybind11>=2.10.3,<3.0.0']

setup_kwargs = {
    'name': 'aclpy',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Masaki Kobayashi',
    'author_email': 'bayashi.cl@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)

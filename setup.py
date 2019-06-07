#!/usr/bin/env python
from setuptools import setup

setup(
  name = 'binance_data',
  packages = ['binance_data'],
  version = 'v0.1.2',
  license='MIT',
  description = 'Python package to retrieve historical data from Binance',
  author = 'Jeff Bingaman',
  author_email = 'bingaman.jeff@gmail.com',
  url = 'https://github.com/uneasyguy/binance_data',
  download_url = 'https://github.com/uneasyguy/binance_data/archive/v0.1.2.tar.gz',
  keywords = ['Binance', 'Cryptocurrency Data', 'OHCLV'],
  install_requires=['python-binance',],
  classifiers=[
    'Topic :: Software Development :: Libraries :: Python Modules',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)

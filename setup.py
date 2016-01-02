__author__ = 'samu'

from setuptools import setup

setup(
    version='1.0',
    name='sandbox',
    install_requires=['Pillow', 'scipy', 'numpy'],
    entry_points={
        'console_scripts': [
            'sandbox_resize_dir = sandbox.images.resize_v3:resize_dir',
        ]},
    packages=['sandbox', 'sandbox.images']
)
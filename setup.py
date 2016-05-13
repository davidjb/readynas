from distutils.core import setup

setup(
    name='readynas',
    version='0.1',
    author='David Beitey',
    author_email=u'qnivq@qnivqwo.pbz'.decode('rot13'),
    packages=['readynas'],
    url='https://github.com/davidjb/readynas',
    license='LICENSE.rst',
    description='Useful functions and utilities for the ReadyNAS.',
    long_description=open('README.rst').read(),
    install_requires=[
        "requests",
    ],
    entry_points={
        'console_scripts': [
	    'readynas-download-config = readynas.frontview:download_configuration_main',
	    'readynas-scroll-string = readynas.frontpanel:scroll_string_main',
	]
    }
)

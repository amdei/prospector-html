# -*- coding: utf-8 -*-

__version__ = '2.0.0'

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from setuptools import find_packages

_PACKAGES = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"])

with open('README.md') as f:
    readme = f.read()

setup(
    name="prospector2html",
    version=__version__,
    author="amDei the Botan",
    author_email="amdeich@gmail.com",
    maintainer="Andrey Kulikov",
    maintainer_email="amdeich@gmail.com",
    license="MIT",
    url="https://github.com/amdei/prospector-html",
    description="HTML report generator for prospector, semgrep, and GitLab SAST static analyzer tools.",
    keywords='prospector semgrep gitlab SAST static code analysis report pylint pyflakes pep8 mccabe frosted',
    long_description=readme,
    long_description_content_type="text/markdown",
    platforms=["any"],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Development Status :: 4 - Beta',
        'Operating System :: Unix',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
        'Topic :: Software Development :: Quality Assurance'
    ],
    packages=_PACKAGES,
    entry_points={
        'console_scripts': [
            'prospector-html = prospector2html.__main__:main',
        ],
    },
    install_requires=[
        'PyYAML',
        'json2html'
    ]
)

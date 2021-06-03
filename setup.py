# -*- coding: utf-8 -*-
"""Installer for the plonetheme.eeq package."""

from setuptools import find_packages
from setuptools import setup


long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    open('CHANGES.rst').read(),
])


setup(
    name='plonetheme.eeq',
    version='1.0a1',
    description="Plone Theme for PSU Educational Equity",
    long_description=long_description,
    # Get more from https://pypi.org/classifiers/
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 5.2",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    keywords='Python Plone CMS',
    author='PSU Educational Equity',
    author_email='par117@psu.edu',
    url='https://github.com/collective/plonetheme.eeq',
    project_urls={
        'PyPI': 'https://pypi.python.org/pypi/plonetheme.eeq',
        'Source': 'https://github.com/collective/plonetheme.eeq',
        'Tracker': 'https://github.com/collective/plonetheme.eeq/issues',
        # 'Documentation': 'https://plonetheme.eeq.readthedocs.io/en/latest/',
    },
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['plonetheme'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    python_requires="==2.7, >=3.6",
    install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
        'plone.app.themingplugins',
        'collective.themefragments',
        'z3c.jbot',
        'plone.api>=1.8.4',
        'plone.restapi',
        'plone.app.dexterity',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            # Plone KGS does not use this version, because it would break
            # Remove if your package shall be part of coredev.
            # plone_coredev tests as of 2016-04-01.
            'plone.testing>=5.0.0',
            'plone.app.contenttypes',
            'plone.app.robotframework[debug]',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    [console_scripts]
    update_locale = plonetheme.eeq.locales.update:update_locale
    """,
)

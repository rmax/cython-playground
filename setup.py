#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob
import os

from pkgutil import walk_packages
from setuptools import setup
from setuptools.extension import Extension
from setuptools.command.build_ext import build_ext as _build_ext


USE_BLACKLIST = bool(os.environ.get('USE_BLACKLIST'))


class build_ext(_build_ext):

    def finalize_options(self):
        from Cython.Build import cythonize
        self.distribution.ext_modules[:] = cythonize(
            self.distribution.ext_modules,
            compiler_directives={'embedsignature': True},
        )
        _build_ext.finalize_options(self)


def load_blacklist(envvar='BLACKLIST_MODULES', filename='blacklist.txt', _missing=object()):
    modules = []
    envval = os.environ.get(envvar, _missing)
    if envval is _missing:
        # Read from file.
        with open(filename) as fp:
            for line in fp:
                if line.startswith('#'):
                    continue
                modules.append(line.strip())
    else:
        # Read from env.
        modules[:] = envval.split()

    return modules


def find_extensions(dir, pattern, **kwargs):
    blacklist = frozenset(load_blacklist())
    for pkgname in find_packages(dir):
        pkgdir = os.path.join(dir, pkgname.replace('.', '/'))
        for path in glob.glob(os.path.join(pkgdir, pattern)):
            name, _ = os.path.splitext(os.path.basename(path))
            modname = '%s.%s' % (pkgname, name)
            if USE_BLACKLIST and modname in blacklist:
                continue
            yield Extension(modname, [path], **kwargs)


def find_packages(path):
    # This method returns packages and subpackages as well.
    for _, name, is_pkg in walk_packages([path]):
        if is_pkg:
            yield name


def read_file(filename):
    with open(filename) as fp:
        return fp.read()


requirements = [
    # TODO: put package requirements here
]

setup(
    name='cython-playground',
    version='0.1.0',
    description="Cython playground for random code examples.",
    long_description=read_file('README.rst') + '\n\n' + read_file('HISTORY.rst'),
    author="Rolando Espinoza",
    author_email='rolando at rmax.io',
    url='https://github.com/rolando/cython-playground',
    packages=list(find_packages('src')),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='cython-playground',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    ext_modules=list(find_extensions('src', '*.pyx')),
    cmdclass={'build_ext': build_ext},
    setup_requires=['cython>=0.24'],
)

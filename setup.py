import os

from setuptools import setup, Extension
from distutils.command.build_ext import build_ext as build_ext_orig


class CTypesExtension(Extension): pass


class BuildExtension(build_ext_orig):

    def build_extension(self, ext):
        self._ctypes = isinstance(ext, CTypesExtension)
        return super().build_extension(ext)

    def get_export_symbols(self, ext):
        if self._ctypes:
            return ext.export_symbols
        return super().get_export_symbols(ext)

    def get_ext_filename(self, ext_name):
        if self._ctypes:
            return ext_name + '.so'
        return super().get_ext_filename(ext_name)


setup(
    name="pyzutil",
    description="z/OS utilities for Python",
    long_description = open("README.md", "r").read(),
    long_description_content_type = 'text/markdown',
    url="https://github.com/daveyc/pyzutil",
    version="0.0.1-2",
    license='MIT',
    maintainer='David Crayford',
    maintainer_email='dcrayford@gmail.com',
    python_requires='>=3.9',
    platforms=['any', 'none'],
    py_modules=["pyzutil", "pyzutil.maps"],
    ext_modules=[
        CTypesExtension(
            "pyzutil.libpyzutil",
            ["libpyzutil.cpp"],
        )
    ],
    cmdclass={'build_ext': BuildExtension},
)

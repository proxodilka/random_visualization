from distutils.core import setup, Extension

module = Extension("crandom", sources=["crandom.c"])

setup(name="PackageName", version="1.0", description="Some desc", ext_modules=[module])

from setuptools import setup
from Cython.Build import cythonize


setup(
    ext_modules=cythonize("binary_vector/**/*.py", exclude=[
                          "binary_vector/__init__.py", "binary_vector/binary_vector_purepy.py"]),
)

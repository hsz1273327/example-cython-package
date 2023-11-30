cythonize -i -3 binary_vector/**/*.pyx


python -m build --sdist

python -m build --wheel --no-isolation


python setup.py build_ext --inplace
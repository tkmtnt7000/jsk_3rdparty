from catkin_pkg.python_setup import generate_distutils_setup
from setuptools import setup

d = generate_distutils_setup(
    packages=['tmp_openai'],
    package_dir={'': 'src'}
)

setup(**d)
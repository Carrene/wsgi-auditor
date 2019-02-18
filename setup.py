import re
from os.path import join, dirname
from setuptools import setup, find_packages


# reading package version (without loading it)
with open(join(dirname(__file__), 'auditor', '__init__.py')) as v_file:
    package_version = re.compile(r".*__version__ = '(.*?)'", re.S)\
        .match(v_file.read()).group(1)


dependencies = [
    'sqlalchemy',
    'bddrest',
    'restfulpy >= 2.7.1',
]


setup(
    name='auditor',
    version=package_version,
    description='A ',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # This is important!
    author='Vahid Mardani',
    author_email='vahid.mardani@gmail.com',
    install_requires=dependencies,
    packages=find_packages(),
    test_suite='.tests',
    license='MIT',

)


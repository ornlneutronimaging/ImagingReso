#!/usr/bin/env python
from setuptools import setup, find_packages
import codecs


def read_file(filename):
    """
    Read a utf8 encoded text file and return its contents.
    """
    with codecs.open(filename, 'r', 'utf8') as f:
        return f.read()


setup(
    name="ImagingReso",
    version="1.7.5",
    author="Yuxuan Zhang, Jean Bilheux",
    author_email="zhangy6@ornl.gov, bilheuxjm@ornl.gov",
    packages=find_packages(exclude=['tests', 'notebooks']),
    package_data={'ImagingReso': ['reference_data/_data_for_unittest/*', 'reference_data/Bonded_H/*']},
    include_package_data=True,
    test_suite='tests',
    install_requires=[
        'numpy==1.24.2',
        'pandas==1.5.3',
        'periodictable==1.5.2',
        'scipy==1.10.1',
        'matplotlib==3.7.1',
        'six==1.16.0',
        'plotly==5.13.1',
    ],
    dependency_links=[
    ],
    description="tool for resonance neutron imaging",
    long_description=read_file('README.rst'),
    license='BSD',
    keywords=['neutron', 'resonance', 'imaging'],
    url="https://github.com/ornlneutronimaging/ImagingReso.git",
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: BSD License',
                 'Topic :: Scientific/Engineering :: Physics',
                 'Intended Audience :: Developers',
                 'Programming Language :: Python :: 3.10',
                 'Natural Language :: English'],
)

# End of file

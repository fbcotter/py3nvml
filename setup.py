from setuptools import setup, find_packages
import os


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


# Read metadata from version file
def get_version():
    f = read("py3nvml/__init__.py")
    for line in f.split('\n'):
        if line.startswith("__version__"):
            return line[15:-1]
    raise Exception("Could not find version number")


setup(name='py3nvml',
      author="Fergal Cotter",
      author_email="fbc23@cam.ac.uk",
      version=get_version(),
      packages=find_packages(),
      description='Python 3 Bindings for the NVIDIA Management Library',
      long_description=read('README.rst'),
      license="BSD",
      url="https://github.com/fbcotter/py3nvml.git",
      download_url="https://github.com/fbcotter/py3nvml/archive/" + get_version() + ".tar.gz",
      scripts=['scripts/py3smi'],
      install_requires=['xmltodict'],
      classifiers=[
          'Programming Language :: Python :: 3.5',
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: BSD License',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: System :: Hardware',
          'Topic :: System :: Systems Administration',
      ],
)

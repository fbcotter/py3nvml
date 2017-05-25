from setuptools import setup, find_packages
import os


def read_file(path):
    with open(os.path.join(os.path.dirname(__file__), path), "r") as fobj:
        return fobj.read()


setup(name='py3nvml',
      version='0.0.3',
      packages=find_packages(),
      description='Python 3 Bindings for the NVIDIA Management Library',
      py_modules=['pynvml', 'nvidia_smi'],
      license="BSD",
      url="https://github.com/fbcotter/py3nvml.git",
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

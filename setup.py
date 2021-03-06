from setuptools import setup, find_packages
from cp93posets import VERSION

setup(
    name='caph1993-posets',
    version=VERSION,
    description='Toolbox for finite posets and lattices',
    url='https://github.com/caph1993/caph1993-posets',
    author='Carlos Pinzón',
    author_email='caph1993@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'caph1993-pytools>=0.4.2',
        'pyhash',
        'pydotplus',
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)
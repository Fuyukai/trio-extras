from pathlib import Path
from setuptools import find_packages, setup

install_requires = [
    "trio>=0.4.0"
]

setup(
    name='trio-extras',
    use_scm_version={
        "version_scheme": "guess-next-dev",
        "local_scheme": "dirty-tag"
    },
    packages=find_packages(),
    url='https://github.com/Fuyukai/trio-extras',
    license='LGPLv3',
    author='Laura Dickinson',
    author_email='l@veriny.tf',
    description='Extra utilities for Trio',
    long_description=Path(__file__).with_name("README.rst").read_text(encoding="utf-8"),
    python_requires=">=3.6.2",
    setup_requires=[
        "setuptools_scm",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Framework :: Trio",
        "Development Status :: 4 - Beta"
    ],
    install_requires=install_requires,
    extras_require={
        "tests": {
            "pytest",
            "pytest-cov",
            "codecov"
        }
    },
)

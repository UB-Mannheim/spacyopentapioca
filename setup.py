#!/usr/bin/env python3

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="spacyopentapioca",
    version='0.1.1',
    author="Renat Shigapov",
    license="MIT",
    description="A spaCy wrapper of OpenTapioca for named entity linking on Wikidata.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/UB-Mannheim/spacyopentapioca",
    install_requires=['spacy>=3.0.0', 'requests>=2.24.0', ],
    packages=find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires='>=3.6',
    entry_points={
        'spacy_factories': 'opentapioca = spacyopentapioca.entity_linker:EntityLinker'
    }
)

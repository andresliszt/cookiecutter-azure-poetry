# -*- coding: utf-8 -*-
"""Build setup."""

import setuptools


with open('README.md') as readme_file:
    readme = readme_file.read()

INSTALL_REQUIRES = [
    "structlog",
    "python-dotenv",
    "pydantic",
]

setuptools.setup(
    name="{{cookiecutter.project_name}}",
    version="{{cookiecutter.version}}",
    author="{{cookiecutter.author_name}}",
    author_email="{{cookiecutter.author_email}}",
    description="{{cookiecutter.project_short_description}}",
    long_description_content_type="text/markdown",
    long_description=readme,
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    install_requires=INSTALL_REQUIRES,
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
)

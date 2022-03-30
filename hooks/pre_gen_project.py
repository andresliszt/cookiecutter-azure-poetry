# -*- coding: utf-8 -*-
"""pre hooks."""

import re

MODULE_REGEX = re.compile(r"^[_a-zA-Z-][_a-zA-Z0-9-]+$")


DOCKER_IMAGE_REGEX = re.compile(r"python:3.\d+")

PACKAGE_NAME = "{{ cookiecutter.package_name }}"

DOCKER_IMAGE = "{{cookiecutter.python_docker_image}}"

if not MODULE_REGEX.match(PACKAGE_NAME):
    raise ValueError(f"Package is not valid python package name. Package name: {PACKAGE_NAME}")

if not DOCKER_IMAGE_REGEX.match(DOCKER_IMAGE):
    raise ValueError(f"Docker image must be a valid python image. Docker image {DOCKER_IMAGE}")
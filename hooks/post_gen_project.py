# -*- coding: utf-8 -*-
"""post hooks."""

import shutil
from pathlib import Path

PROJECT_DIRECTORY = Path(".").absolute()


def remove(filepath: Path):
    target = PROJECT_DIRECTORY / filepath

    if target.is_dir():
        shutil.rmtree(target, ignore_errors=True)
    else:
        target.unlink()


if __name__ == "__main__":

    if "{{ cookiecutter.add_sphinx }}" == "no":
        remove("docs")

    if "{{ cookiecutter.use_tox }}" == "no":
        remove("tox.ini")

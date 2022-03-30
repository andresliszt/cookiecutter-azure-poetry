# -*- coding: utf-8 -*-
"""Testing cookiecutter template.

The main ideas of these tests are taken from the repository
`https://github.com/johanvergeer/cookiecutter-poetry/`


"""

from pathlib import Path
from pytest_cookies.plugin import Cookies, Result

import pytest

PROJECT_ROOT_DIR = Path(__file__).parent.parent
"""Root dir where is placed cookiecutter.json file"""


def list_directories(directory):
    return [f.name for f in directory.iterdir()]

@pytest.yield_fixture
def bake_result(request, cookies: Cookies):
    """Build test project as pytest fixture"""
    param = request.param if hasattr(request, "param") else None
    result = cookies.bake(template=str(PROJECT_ROOT_DIR), extra_context = param)
    yield result

@pytest.mark.parametrize("bake_result", ([{"project_name": "test-project"}]), indirect=True)
def test_bake_with_defaults(bake_result: Result) -> None:
    assert bake_result.project_path.is_dir()
    assert bake_result.project_path.name == "test-project"
    directories = list_directories(bake_result.project_path)
    assert "pyproject.toml" in directories
    assert "test_project" in directories
    assert "tox.ini" in directories
    assert "tests" in directories
    assert "docs" in directories
    assert ".dockerignore" in directories
    assert "README.md" in directories
    assert "setup.py" in directories
    assert "azure-pipelines.yml" in directories
    assert "Dockerfile" in directories
    # Check .py files at package
    py_files = list_directories(Path(bake_result.project_path, "test_project"))
    assert "__init__.py" in py_files
    assert "settings.py" in py_files
    assert "logger.py" in py_files
    assert "exc.py" in py_files

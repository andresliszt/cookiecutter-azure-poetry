# cokiecutter-azure-poetry

[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


Cookiecutter template for managing project with poetry with continuous integration in Azure.

Docker multistage build for testing, build documentation with [sphinx](https://www.sphinx-doc.org/en/master/) and publish package as Azure artifact using [twine](https://docs.microsoft.com/en-us/azure/devops/pipelines/tasks/package/twine-authenticate?view=azure-devops) authentication.

## Features

-   [Poetry](https://python-poetry.org/)  package manager.
-   [Tox](https://tox.wiki/en/latest/) virtual environment manager, code formatting with [black](https://github.com/psf/black), [autpep8](https://github.com/hhatto/autopep8), [isort](https://pycqa.github.io/isort/) and [docformatter](https://github.com/PyCQA/docformatter) and linting using [pylint](https://pylint.org/), [bandit](https://github.com/PyCQA/bandit), [flake8](https://flake8.pycqa.org/en/latest/) and [mypy](https://mypy.readthedocs.io/en/stable/) 
-   Env vars loaded using [python-dotenv](https://github.com/theskumar/python-dotenv) from ``.env`` file.
-   Logger configured using [structlog](https://www.structlog.org/en/stable/) to save in json format and track function execution.
-   [Pydantic](https://pydantic-docs.helpmanual.io/) integration in settings as a class that inherits from ``pydantic.BaseSettings``.

## Azure pipelines

Simple continiuous integration using [Docker Tasks](https://docs.microsoft.com/en-us/azure/devops/pipelines/tasks/build/docker?view=azure-devops) to test and publish as an Azure Artifact. The ``Dockerfile`` contains 3 steps, the first one called *base* install only productive dependencies, the second one called *tester* copy inside the ``tests`` folder and run ``pytest`` and finally the last called *publisher* build the package wheel and publish into the private repository. This last step only makes sense to be executed inside the pipeline because it uses a file
that the [twine](https://docs.microsoft.com/en-us/azure/devops/pipelines/tasks/package/twine-authenticate?view=azure-devops) authentication creates at `${PYPIRC_PATH}`, which contain the needed credentials. The build is not done using the command ``poetry build`` but rather it goes through the ``setup.py`` file. 


## Pydantic settings

Project settings are controlled by pydantic at ``my_package.settings.py``. If an env var is need to be set you have to edit the class ``my_package.settings.Settings``, for example, suposse you have to add a connection string for some database system as an env var, then

```python

# Other imports are here but we don't write them in this example

from pydantic import SecretStr

class Settings(BaseSettings):
    """Project settings variables."""

    PACKAGE_PATH = Path(__file__).parent
    """Package path (python files)."""

    PROJECT_PATH = PACKAGE_PATH.parent
    """Project path (all files)."""
    
    LOG_PATH: Optional[Path]
    """Path to logfile, only works if ``LOG_DESTINATION=FILE``."""
    
    LOG_FORMAT: LogFormatter = LogFormatter.COLOR.value
    """Log style."""
    
    LOG_LEVEL: LogLevel = LogLevel.INFO.value
    """Log level from ``logging`` module."""
    
    LOG_DESTINATION: LogDest = LogDest.CONSOLE.value
    """Destination for logs."""
    
    CONNECTION_STRING: SecretStr # This is a new mandatory env var

    class Config:
        """Inner configuration."""

        env_prefix = "MY_PACKAGE_" # All env vars with this prefix
        use_enum_values = True

```


You have 3 options to set the value for ``CONNECTION_STRING``, the first one is write inside the class definition (not recommended for passwords!), the second one is use ``export`` command or ``set`` in Windows to set the value of the variable and the easiest is to write it in the configuration file `.env` at the root of the project. Environment variables are prefixed with
``MY_PACKAGE_``, i.e. the name of the package in uppercase. Example of `.env` file with a simple postgres connection string


```.env
# .env file

MY_PACKAGE_CONNECTION_STRING=postgresql://foo:bar@localhost:5432/mydatabase

```

The project settings are in the top level ``__init__``, to use it you have to import ``SETTINGS`` object


```python

from sqlalchemy import create_engine

from my_package import SETTINGS # Here SETTINGS is an instance of ``my_package.settings.Settings``

engine = create_engine(SETTINGS.CONNECTION_STRING.get_secret_value()) # We declared the connection as SecretStr!

```


## Tox

Tox is use to create virtual environment, to clear all temporary files (as ``__pycache__``), to format the code and lint the code. Here the list of avialables commands


```sh
# Creates a virtual environment using the python version declared in the build of cookiecutter, obiously must exist in the system otherwise error will be raised
tox -e venv

# Delete all temporary files
tox -e clear

# Format code using black, isort, docformatter and autopep8
tox -e format

# Lint code using pylint, mypy, bandit and flake8
tox -e lint

```

> :warning: **The virtual environment mus be created** with ``tox -e venv`` to use other commands, otherwise could be unexpected behavior!


## Logging

A nice logger is configured using ``structlog``. The logger can be controlled in the setting class through the attributes ``LOG_FORMAT`` with possible values ``JSON`` or ``COLOR`` (the last requires [colorama](https://github.com/tartley/colorama)). ``LOG_DESTINATION`` with possible values ``CONSOLE`` or ``FILE``, if ``FILE`` is seted must also be seted ``LOG_PATH``, the file where to save. ``LOG_LEVEL``, which is the level of the logger and is the same of [logging](https://docs.python.org/3/library/logging.html) module. 

Also the logger is 


```.env
# .env file

MY_PACKAGE_LOG_LEVEL=20
MY_PACKAGE_LOG_DESTINATION=CONSOLE
MY_PACKAGE_LOG_FORMAT=JSON

```

The logger admits any ``kwarg`` argument to add more information, for example printing in console


```python

from my_package import logger

logger.info("This is an exmaple log", example_kwargs = "this is an example kwarg", other_example_kwargs = "this is other example kwarg")

>>> 2022-03-29T18:40:54.646488Z [info     ] This is an exmaple log         [pymooslotting] example_kwargs=this is an example kwarg other_example_kwargs=this is other example kwarg
```

Other levels are ``logger.warning``, ``logger.debug`` and ``logger.error``.



## TODO

-   Test the cookiecutter project.
-   Add public option for CI/CD like travis or github actions. 
-   Add sphinx into CI/CD to publish documentation.
-   Write a better readme.
-   Write a better TODO.
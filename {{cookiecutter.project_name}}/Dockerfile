FROM {{cookiecutter.python_docker_image}} as base
WORKDIR /{{cookiecutter.package_name}}
COPY pyproject.toml ./
ADD /{{cookiecutter.package_name}} ./{{cookiecutter.package_name}}
ENV PYTHONPATH "${PYTHONPATH}:./"
RUN python -m pip install --upgrade pip \
    && pip install poetry \
    &&poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi
# Test image
FROM base as tester
COPY tests ./tests
RUN pip install pytest && pytest -s -vvv
{%- if cookiecutter.publish_in == 'Private PyPI'%}
# Publish Image
FROM base as publisher
ARG ARTIFACT_FEED
ADD PYPIRC / 
RUN pip install wheel twine \
    && poetry build \
    && python -m twine upload --verbose -r ${ARTIFACT_FEED} --config-file /PYPIRC dist/*.whl
{%- endif %}
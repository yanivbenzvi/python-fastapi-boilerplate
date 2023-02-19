###############################################
# Base Image
###############################################
FROM python:3.10.4-slim as python-base

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    build-essential \
    pkg-config


ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.1.13 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/app" \
    VENV_PATH="/app/.venv"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

###############################################
# Poetry Image
###############################################
FROM python-base as poetry
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    git \
    openssl

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://install.python-poetry.org | python -

###############################################
# Production Application Builder
###############################################
FROM poetry as builder

# copy project requirement files here to ensure they will be cached.
WORKDIR $PYSETUP_PATH
# RUN poetry config settings.virtualenvs.in-project true
COPY poetry.lock pyproject.toml ./

# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN poetry install --no-dev


###############################################
# Production Image Builder
###############################################
FROM python-base as production

RUN groupadd -g 999 python && \
    useradd -r -u 999 -g python python

RUN chown python:python .
RUN mkdir usage_files

COPY --chown=python:python ./app/ $PYSETUP_PATH
COPY --chown=python:python --from=builder $VENV_PATH $VENV_PATH
EXPOSE 8000

USER 999

CMD ["gunicorn", "app.main:app", "-c", "app/gunicorn_config.py"]
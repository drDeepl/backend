FROM python:3.8-slim-bullseye AS development_build

ENV BUILD_ONLY_PACKAGES='wget' \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1 \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100


# System deps:
RUN apt-get update \
  && apt-get install --no-install-recommends -y \
    bash \
    build-essential \
    curl \
    gettext \
    git \
    libpq-dev \
    # Defining build-time-only dependencies:
    # $BUILD_ONLY_PACKAGES \
  # Installing `poetry` package manager:
  # https://github.com/python-poetry/poetry
  && pip install pipenv \
  # Removing build-time-only dependencies:
  # && apt-get remove -y $BUILD_ONLY_PACKAGES \
  # Cleaning cache:
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && apt-get clean -y && rm -rf /var/lib/apt/lists/*

WORKDIR /code

# Copy only requirements, to cache them in docker layer
COPY ./Pipfile.lock ./Pipfile /code/

RUN pip3 install uvicorn meinheld psycopg2 backports.weakref

# Project initialization:
RUN pipenv install --system --deploy --ignore-pipfile

COPY . /code/

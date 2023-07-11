FROM python:3.10

RUN apt-get update -y

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/usr/local python3 -

RUN python -m venv /venv
RUN . /venv/bin/activate
RUN pip install allure-pytest

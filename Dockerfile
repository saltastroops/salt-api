# Dockerfile for creating the SALT API server

# WARNING: This Dockerfile is not suitable for production use.

# Based on https://fastapi.tiangolo.com/deployment/docker/

FROM python:3.9

# LABEL specifies the File Author / Organization
LABEL author="SALT Software Team <saltsoftware@saao.ac.za>"

EXPOSE 80

WORKDIR /app

RUN apt-get update -y
RUN apt-get install -y default-jre
RUN apt-get install -y ghostscript
RUN apt-get install -y imagemagick
RUN apt-get install -y wkhtmltopdf

# Give ImageMagick access to pdf files
RUN sed -i "s@<policy domain=\"coder\" rights=\"none\" pattern=\"PDF\" />@<policy domain=\"coder\" rights=\"read|write\" pattern=\"PDF\" />@g" /etc/ImageMagick-6/policy.xml

RUN pip install wheel

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* ./

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

RUN pip uninstall -y poetry

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./saltapi /app/saltapi

RUN mkdir /var/www
RUN mkdir /var/www/.astropy
RUN chown www-data:www-data /var/www/.astropy

USER www-data:www-data

RUN mkdir /tmp/.PIPT

CMD ["uvicorn", "saltapi.main:app", "--host", "0.0.0.0", "--port", "80"]

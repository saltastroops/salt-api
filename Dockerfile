# Dockerfile for creating the SALT API server

# WARNING: This Dockerfile is not suitable for production use.

# Based on https://fastapi.tiangolo.com/deployment/docker/

FROM python:3.10

LABEL org.opencontainers.image.authors="SALT Software Team <saltsoftware@saao.ac.za>"

EXPOSE 80

WORKDIR /app

RUN apt-get update -y \
 && apt-get install -y --no-install-recommends default-jre=2:1.17-74 \
 && apt-get install -y --no-install-recommends ghostscript=10.0.0~dfsg-11+deb12u5 \
 && apt-get install -y --no-install-recommends imagemagick=8:6.9.11.60+dfsg-1.6+deb12u2 \
 && apt-get install -y --no-install-recommends wkhtmltopdf=0.12.6-2+b1 \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* \
 && sed -i "s@<policy domain=\"coder\" rights=\"none\" pattern=\"PDF\" />@<policy domain=\"coder\" rights=\"read|write\" pattern=\"PDF\" />@g" /etc/ImageMagick-6/policy.xml \
  && pip install --no-cache-dir wheel==0.44.0 \
  && pip install --no-cache-dir poetry==1.8.4

COPY ./pyproject.toml ./poetry.lock* ./

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes \
 && pip uninstall -y poetry \
 && pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./saltapi /app/saltapi

RUN mkdir /var/www \
 && mkdir /var/www/.astropy \
 && chown www-data:www-data /var/www/.astropy

USER www-data:www-data

RUN mkdir /tmp/.PIPT

CMD ["uvicorn", "saltapi.main:app", "--host", "0.0.0.0", "--port", "80"]

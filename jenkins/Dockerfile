FROM python:3.9

RUN apt-get update -y
RUN apt-get install -y default-jre
RUN apt-get install -y ghostscript
RUN apt-get install -y imagemagick
RUN apt-get install -y wkhtmltopdf

# Give ImageMagick access to pdf files
RUN sed -i "s@<policy domain=\"coder\" rights=\"none\" pattern=\"PDF\" />@<policy domain=\"coder\" rights=\"read|write\" pattern=\"PDF\" />@g" /etc/ImageMagick-6/policy.xml

python -m pip install poetry

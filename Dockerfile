# pull official base image
FROM python:3.8.10-buster

# set work directory
WORKDIR /usr/src/pharmacy

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y netcat-openbsd gcc openssl && \
    apt-get install -y gdal-bin binutils libproj-dev libgdal-dev && \
    apt-get install -y libpq-dev postgresql-client python-gdal python3-gdal && \
    apt-get clean all && rm -rf /var/apt/lists/* && rm -rf /var/cache/apt/*


RUN apt-get install -y tesseract-ocr 
RUN apt-get install -y libtesseract-dev
RUN apt-get install -y tesseract-ocr-jpn


# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/pharmacy/requirements.txt
RUN pip install -r /usr/src/pharmacy/requirements.txt

COPY ./ocr_req.txt /usr/src/pharmacy/ocr_req.txt
RUN pip install -r /usr/src/pharmacy/ocr_req.txt

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

# copy project
COPY . /usr/src/pharmacy/
VOLUME /usr/src/pharmacy/media

# Trigram Search
# RUN apt-get install postgresql-contrib-8.4
# psql -U pharmacy -d pharmacy -f /usr/share/postgresql/8.4/contrib/pg_trgm.sql
RUN apt-get install -y cron

# run entrypoint.sh
RUN ["chmod", "+x", "/usr/src/pharmacy/entrypoint.sh"]

ENTRYPOINT ["sh","/usr/src/pharmacy/entrypoint.sh"]


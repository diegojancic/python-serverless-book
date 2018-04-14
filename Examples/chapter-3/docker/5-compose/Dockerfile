FROM python:3.6-alpine

COPY requirements.txt /

EXPOSE 80


RUN set -ex \
    && apk add --no-cache python-dev gcc musl-dev postgresql-dev

#RUN set -ex \
#    && apk add --no-cache \
#            python-dev \
#            gcc \
#            make \
#            libc-dev \
#            musl-dev \
#            linux-headers \
#            pcre-dev \
#            postgresql-dev

RUN pip install virtualenv \
    && virtualenv /var/venv \
    && source /var/venv/bin/activate \
    && pip install -r requirements.txt

RUN mkdir /code/
WORKDIR /code/
COPY . /code/

CMD ["sh", "docker-entrypoint.sh"]

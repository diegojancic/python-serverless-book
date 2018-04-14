FROM python:3.6-alpine

# Copy in your requirements file
COPY requirements.txt /requirements.txt

# Install build deps, then run `pip install`, then remove unneeded build deps all in a single step. Correct the path to your production requirements file, if needed.
RUN set -ex \
    && apk add --no-cache --virtual .build-deps \
            python-dev \
            gcc \
            make \
            libc-dev \
            musl-dev \
            linux-headers \
            pcre-dev \
            postgresql-dev \
    && LIBRARY_PATH=/lib:/usr/lib /bin/sh -c "pip install virtualenv uwsgi awscli" \
    && virtualenv /var/venv  \
    && source /var/venv/bin/activate \
    && pip install -r /requirements.txt \
    && deactivate \
    && runDeps="$( \
            scanelf --needed --nobanner --recursive /usr/local \
                    | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
                    | sort -u \
                    | xargs -r apk info --installed \
                    | sort -u \
    )" \
    && apk add --virtual .python-rundeps $runDeps \
    && apk del .build-deps 
    
    
# Copy your application code to the container (make sure you create a .dockerignore file if any large files or directories should be excluded)
RUN mkdir /code/
WORKDIR /code/
COPY . /code/

# uWSGI will listen on this port
EXPOSE 8000

# Add any custom, static environment variables needed by Django or your settings file here:
ENV DJANGO_SETTINGS_MODULE=website.settings

# uWSGI configuration (customize as needed):
ENV UWSGI_WSGI_FILE=website/wsgi.py UWSGI_HTTP=:8000 UWSGI_MASTER=1 UWSGI_WORKERS=2 UWSGI_THREADS=8 UWSGI_UID=1000 UWSGI_GID=2000 UWSGI_LAZY_APPS=1 UWSGI_WSGI_ENV_BEHAVIOR=holy

# Call collectstatic (customize the following line with the minimal environment variables needed for manage.py to run):
#RUN DATABASE_URL=none /venv/bin/python project/manage.py collectstatic --noinput

# Set database file as read-write
RUN chmod a+w db.sqlite3
RUN chmod a+w .


# Start uWSGI
CMD ["/usr/local/bin/uwsgi", "--http-auto-chunked", "--http-keepalive", "-H", "/var/venv"]

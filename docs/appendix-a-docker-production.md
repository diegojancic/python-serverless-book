# Appendix A: Running Docker in Production

This is not intended to be a guide on all the necessary measures and settings that need to be taken care of to run a web application in production using Docker. We will try to provide, instead, a starting point for a set of possible configurations using uWSGI and NGINX.

## Why Do We Need 2 Servers?

It is recommended—not to say, absolutely necessary—to use 2 different web servers because each of them follows the Unix philosophy of "*Do One Thing and Do It Well*".

uWSGI is used to serve WSGI, or "Python Web Server Gateway Interface", applications. The uWSGI serves the dynamic requests from our Python code very well, but it doesn't do a great job in certain cases. Because its worker processes are assigned to a single connection until the response is sent, responding to static content or slow clients can lock the server fairly quickly. On the other hand, the NGINX server is specifically prepared to serve multiple requests in parallel and cache responses.

We will be setting up 2 servers then: an NGINX server used as a proxy between the client and the actual Python application, and the regular web application server.

We will create 2 folders, one called proxy for NGINX and one called server for our application.

## Configuration Files

These are our configuration files for the proxy:

**proxy/default.conf**
```nginx
server {
  listen 80;
  location / {
    proxy_pass http://server:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
  }
}
```

**proxy/Dockerfile**
```dockerfile
FROM nginx
COPY default.conf /etc/nginx/conf.d/
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

And for the server:

**server/Dockerfile**
```dockerfile
FROM python:3.6-alpine

COPY requirements.txt /requirements.txt

# Install build deps, then run 'pip install', then remove unneeded build deps all in a single step.
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

# Set database file as read-write
RUN chmod a+w db.sqlite3
RUN chmod a+w .

# Start uWSGI
CMD ["/usr/local/bin/uwsgi", "--http-auto-chunked", "--http-keepalive", "-H", "/var/venv"]
```

Please note that this example is still using SQLite as a database backend. For production you should use a database server such as PostgreSQL, MariaDB, or similar.

## Building and Running

To build and run both servers, run (output omitted):

```bash
cd server
docker build -t aws-server .
docker run -d -p 8000:8000 --name aws-server aws-server

cd ../proxy
docker build -t aws-proxy .
docker run -p 80:80 --link aws-server:server --name aws-proxy aws-proxy
```

There you should have 2 containers running both the application server and the proxy.

## Production Considerations

This configuration provides a basic setup for running Django applications with Docker in production. For a fully production-ready setup, consider the following additional configurations:

### Security
- Use HTTPS/TLS certificates
- Configure proper firewall rules
- Implement rate limiting
- Use secrets management for sensitive data

### Performance
- Configure caching (Redis/Memcached)
- Optimize database connections
- Implement monitoring and logging
- Use health checks

### Scalability
- Implement container orchestration (Kubernetes, Docker Swarm)
- Use load balancers
- Implement auto-scaling policies
- Configure persistent storage

### Monitoring
- Set up application monitoring
- Configure log aggregation
- Implement alerting
- Use performance monitoring tools

This appendix provides a foundation for Docker deployment, but production systems require additional considerations based on specific requirements and scale.

---

[← Previous: Chapter 9 - Understanding Function Performance](09-understanding-function-performance.md) | [Back to Table of Contents ↑](README.md)